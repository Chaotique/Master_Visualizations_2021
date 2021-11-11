import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
import pandas as pd
from sodapy import Socrata # Was not in the installation list for this course!
                           #Use "pip install sodapy" or "conda install sodapy" to install
import geopandas as gpd
import pandas_bokeh
import matplotlib.pyplot as plt
pandas_bokeh.output_notebook()
from bokeh.plotting import figure, output_file, save


#First:
#create sidebar


gender = st.sidebar.selectbox(
    "Which gender do you want to display?",
    ("Home", "Dona", "All")
)

scraping_depth = st.sidebar.number_input("How deep do you want to scrape?", value=2000, step=1000)


#Second:
#Load data


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("analisi.transparenciacatalunya.cat", None)
print("Format of dataset: ", type(client))

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("irki-p3c7", limit=2000) # 2000 is the number of vaccinated patients that we scrape from the web page

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# filter dataframe for gender
if gender in ["Home", "Dona"]:
    filtered_df = results_df[results_df["sexe"]==gender]
else:
    filtered_df = results_df


#Third:
#create page


st.write("""# Our very own Dashboard
Find some interactive stats on Catalunya!
""")

cp_barna  = gpd.read_file("ds-codigos-postales-master/data/BARCELONA.geojson" )
cp_lleida = gpd.read_file("ds-codigos-postales-master/data/LLEIDA.geojson" )
cp_tarragona = gpd.read_file("ds-codigos-postales-master/data/TARRAGONA.geojson" )
cp_girona = gpd.read_file("ds-codigos-postales-master/data/GIRONA.geojson" )
cp = gpd.GeoDataFrame(pd.concat([cp_barna, cp_lleida, cp_tarragona, cp_girona], ignore_index=True), crs=cp_barna.crs)

pc = list(filtered_df["municipi_codi"])
print(len(pc)) #COD_POSTAL

# how often does each cp appear in pc?
occurrences = [pc.count(x) for x in pc]

# Sample data to plot
df=pd.DataFrame({'COD_POSTAL': pc, 'A':occurrences})

# Join ontario dataset with sample data
new_df = gpd.GeoDataFrame(cp.merge(df, on=['COD_POSTAL']), crs=cp_barna.crs)

p = new_df.plot_bokeh(simplify_shapes=0, category="A", colormap="Spectral", legend = "participants postal codes", hovertool_columns=["COD_POSTAL"])#, colormap="Spectral")

st.bokeh_chart(p)

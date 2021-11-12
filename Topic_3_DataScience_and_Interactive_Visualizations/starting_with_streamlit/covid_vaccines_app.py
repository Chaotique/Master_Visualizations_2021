import streamlit as st
import pandas as pd
import numpy as np
from sodapy import Socrata # Was not in the installation list for this course!
                           # Use "pip install sodapy" or "conda install sodapy" to install
from plots.geo_plot_vaccines import plot_abundance_for_list_of_postal_codes


#First:
#create sidebar 

gender = st.sidebar.selectbox(
    "Which gender do you want to display?",
    ("all", "male", "female")
)

scraping_depth = st.sidebar.number_input("How deep do you want to scrape?", value=2000, step=1000)


# Second:
# Load data and apply filters according to settings in sidebar


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("analisi.transparenciacatalunya.cat", None)
#print("Format of dataset: ", type(client))

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
vaccinated_per_postal_code = client.get("irki-p3c7", limit=scraping_depth) # 2000 is the number of vaccinated patients that we scrape from the web page

# Convert to pandas DataFrame
vacc_ppc_df = pd.DataFrame.from_records(vaccinated_per_postal_code)

# gender translation
dict_gender = {"male": "Home",
               "female": "Dona",
               "all": "all"}
# filter dataframe for gender
if dict_gender[gender] in ["Home", "Dona"]:
    filtered_df = vacc_ppc_df[vacc_ppc_df["sexe"]==dict_gender[gender]]
else:
    filtered_df = vacc_ppc_df


#Third:
#create page and load plots


st.write("""# Our very own Dashboard
Find some interactive stats on Catalunya!
""")

# Bokeh plot with vaccinated per postal_code
pc = list(filtered_df["municipi_codi"])

p = plot_abundance_for_list_of_postal_codes(pc)


st.bokeh_chart(p)

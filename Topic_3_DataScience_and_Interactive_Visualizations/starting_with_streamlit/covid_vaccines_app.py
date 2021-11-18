import streamlit as st
import pandas as pd
import numpy as np
from sodapy import Socrata # Was not in the installation list for this course!
                           # Use "pip install sodapy" or "conda install sodapy" to install
from plots.geo_plot_vaccines import plot_abundance_for_list_of_postal_codes
import datetime


#First:
#create sidebar 

gender = st.sidebar.selectbox(
    "Which gender do you want to display?",
    ("all", "male", "female")
)

scraping_depth = st.sidebar.number_input("How deep do you want to scrape?", value=2000, step=1000)

s = st.sidebar.button('Click here, please.')
d = st.sidebar.date_input(
    "When's your birthday",
    datetime.date(2019, 7, 6))
color = st.sidebar.color_picker('Pick A Color', '#00f900')
dr = st.sidebar.date_input("select a range of datesdates", [])


# Second:
# Load data and apply filters according to settings in sidebar

@st.cache(allow_output_mutation=True)
def load_data_base(scraping_depth):
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("analisi.transparenciacatalunya.cat", None)
    #print("Format of dataset: ", type(client))

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    vaccinated_per_postal_code = client.get("irki-p3c7", limit=scraping_depth) # 2000 is the number of vaccinated patients that we scrape from the web page

    # Convert to pandas DataFrame
    vacc_ppc_df = pd.DataFrame.from_records(vaccinated_per_postal_code)
    return vacc_ppc_df
vacc_ppc_df = load_data_base(scraping_depth)

@st.cache(allow_output_mutation=True)
def filter_for_gender(gender, vacc_ppc_df):
    # gender translation
    dict_gender = {"male": "Home",
                "female": "Dona",
                "all": "all"}
    # filter dataframe for gender
    if dict_gender[gender] in ["Home", "Dona"]:
        filtered_df = vacc_ppc_df[vacc_ppc_df["sexe"]==dict_gender[gender]]
    else:
        filtered_df = vacc_ppc_df
    return filtered_df
filtered_df = filter_for_gender(gender, vacc_ppc_df)


#Third:
#create page and load plots


st.write("""# Our very own Dashboard
Find some interactive stats on Catalunya!
""")

st.write("This is the plot filtered for gender that is only reloaded when gender or scraping_depth are altered by the user.")

@st.cache(allow_output_mutation=True)
def plot_abundance_filtered(filtered_df):
    # Bokeh plot with vaccinated per postal_code
    pc = list(filtered_df["municipi_codi"])
    p_nr = plot_abundance_for_list_of_postal_codes(pc)
    return p_nr
p_nr = plot_abundance_filtered(filtered_df)
st.bokeh_chart(p_nr)

st.write("This is a plot that reloads anytime the user inteacts with the widgets.")
pc = list(vacc_ppc_df["municipi_codi"]) # even though it get's the unfiltered DataFrame (so even though it does not depend on gender), it reloads any time the user klicks sth.
p = plot_abundance_for_list_of_postal_codes(pc)
st.bokeh_chart(p)

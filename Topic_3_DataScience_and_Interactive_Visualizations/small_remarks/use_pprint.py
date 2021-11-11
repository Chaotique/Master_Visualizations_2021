"""
use pprint for a more beatiful output of pandas DataFrames
"""
import pandas as pd
from pprint import pprint

df = pd.DataFrame()
df["Country"]  = ["UK",     "France", "Spain"]
df["Capital"] = ["London", "Paris", "Madrid"]
df["Inhabitants Country in Mio"] = [67.22, 67.39, 47.35]
pprint(df)

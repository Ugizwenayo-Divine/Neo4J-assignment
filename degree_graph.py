import pandas as pd
import plotly.express as px

df = pd.read_csv("degrees.csv")

counts = df["degree"].value_counts().sort_index()

fig = px.bar(x=counts.index, y=counts.values, labels={"x": "Degree", "y": "Number of Intersections"})

fig.show()

import altair as alt
from vega_datasets import data

import datapane as dp

df = data.cars()

plot1 = (
    alt.Chart(df)
    .mark_circle(size=60)
    .encode(
        x="Horsepower",
        y="Miles_per_Gallon",
        color="Origin",
        tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
    )
    .interactive()
)

app = dp.App(dp.Plot(plot1), dp.DataTable(df))
app.upload(name="My example app")

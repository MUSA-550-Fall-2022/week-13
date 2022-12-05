import io

import altair as alt
import dash
import pandas as pd
from dash import dcc, html

# load the data
penguins = pd.read_csv(
    "https://raw.githubusercontent.com/MUSA-550-Fall-2022/week-2/master/data/penguins.csv"
)

# initialize the app
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# set a title
app.title = "Testing Dash and Altair"

# columns to plot
COLUMNS = [
    "flipper_length_mm",
    "bill_length_mm",
    "body_mass_g",
    "bill_depth_mm",
]
LABELS = ["Flipper Length", "Bill Length", "Body Mass", "Bill Depth"]

# set the layout
app.layout = html.Div(
    [
        html.Div(
            [
                # Dropdown for x axis
                html.Div(
                    [
                        html.Label("x-axis"),
                        dcc.Dropdown(
                            id="x_axis",
                            options=[
                                {"label": LABELS[i], "value": col}
                                for i, col in enumerate(COLUMNS)
                            ],
                            value="flipper_length_mm",
                        ),
                    ],
                    style={
                        "width": "250px",
                        "margin-right": "auto",
                        "margin-left": "auto",
                        "text-align": "center",
                    },
                ),
                # Dropdown for y axis
                html.Div(
                    [
                        html.Label("y-axis"),
                        dcc.Dropdown(
                            id="y_axis",
                            options=[
                                {"label": LABELS[i], "value": col}
                                for i, col in enumerate(COLUMNS)
                            ],
                            value="bill_length_mm",
                        ),
                    ],
                    style={
                        "width": "250px",
                        "margin-right": "auto",
                        "margin-left": "auto",
                        "text-align": "center",
                    },
                ),
            ],
        ),
        # This is where the chart goes
        html.Iframe(
            id="plot",  # this matches below!
            srcDoc=None,
            height="500",
            width="1000",
            sandbox="allow-scripts",
            style={"border-width": "0px"},
        ),
    ],
    style={"display": "flex", "justify-content": "center"},
)


@app.callback(
    dash.dependencies.Output("plot", "srcDoc"),  # output
    [
        dash.dependencies.Input("x_axis", "value"),  # input 1
        dash.dependencies.Input("y_axis", "value"),  # input 2
    ],
)
def render(x_axis, y_axis):

    brush = alt.selection_interval()
    base = alt.Chart(penguins)

    # scatter plot of x vs y
    scatter = (
        base.mark_point()
        .encode(
            x=alt.X(x_axis, scale=alt.Scale(zero=False)),
            y=alt.Y(y_axis, scale=alt.Scale(zero=False)),
            color="species:N",
        )
        .properties(width=300, height=400, selection=brush)
    )

    # histogram of body mass
    hist = (
        base.mark_bar()
        .encode(x=alt.X("body_mass_g:Q", bin=True), y="count()", color="species:N")
        .transform_filter(brush.ref())
    ).properties(width=300, height=400)

    # the combined chart
    chart = alt.hconcat(scatter, hist)

    # SAVE TO HTML AND THEN RETURN
    # Save html as a StringIO object in memory
    chart_html = io.StringIO()
    chart.save(chart_html, "html")

    # Return the html from StringIO object
    return chart_html.getvalue()


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5555, debug=True)

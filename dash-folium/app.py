import carto2gpd
import dash
import folium
from dash import dcc, html
from folium.plugins import HeatMap

# initialize the app
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# set a title
app.title = "Dash + Folium: Philadelphia Shootings"


def get_data(days):
    """
    Query the CARTO database to get shootings from the recent past.

    Parameters
    ----------
    days : int
        the number of days to get data for

    Returns
    -------
    gdf : GeoDataFrame
        the data frame holding the queried data
    """
    # Query for the data
    URL = "https://phl.carto.com/api/v2/sql"
    WHERE = f"date_ >= current_date - {days}"
    gdf = carto2gpd.get(URL, "shootings", where=WHERE)

    # Add lat/lng columns
    gdf["lat"] = gdf.geometry.y
    gdf["lng"] = gdf.geometry.x

    # Remove rows with missing geo coordinates
    gdf = gdf.dropna(subset=["lat", "lng"])

    return gdf


def get_folium_map(data, days):
    """
    Make the Folium map
    """
    # initialize the Folium map
    m = folium.Map(location=[39.99, -75.13], tiles="Cartodb Positron", zoom_start=12)

    # convert to coordinates array
    coordinates = data[["lat", "lng"]].values

    # add heat map
    HeatMap(coordinates).add_to(m)

    # IMPORTANT: return the string version of the HTML file
    # SPECIFIC TO FOLIUM
    return m.get_root().render()


markdown_text = """
# Shootings in Philadelphia
"""

# set the layout
app.layout = html.Div(
    [
        # the title!
        dcc.Markdown(markdown_text),
        # DIV ELEMENT FOR DAYS SLIDER
        html.Div(
            [
                html.Label("Select the number of days to query"),
                dcc.Slider(id="daysSlider", min=30, max=365, value=90),
                html.P(id="daysSliderValue", children=""),
            ],
            style={
                "width": "250px",
                "margin-right": "auto",
                "margin-left": "auto",
                "text-align": "center",
            },
        ),
        # MAP IFRAME
        html.Div(
            [
                html.Iframe(
                    id="map",
                    srcDoc=None,
                    height="500",
                    width="800",
                    sandbox="allow-scripts",
                    style={"border-width": "0px", "align": "center"},
                )
            ],
            style={"display": "flex", "justify-content": "center"},
        ),
    ]
)


@app.callback(
    [
        dash.dependencies.Output("map", "srcDoc"),
        dash.dependencies.Output("daysSliderValue", "children"),
    ],
    [dash.dependencies.Input("daysSlider", "value")],
)
def render(days):

    # query the CARTO database
    gdf = get_data(days)

    # make and return our map
    map = get_folium_map(gdf, days)

    text = f"Days = {days}"

    return map, text


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5555, debug=True)

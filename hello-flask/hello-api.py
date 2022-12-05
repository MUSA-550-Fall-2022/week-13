import carto2gpd
import geopandas as gpd
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/shootings/")
def hello(days=90, fatal=0):
    """
    Two optional request parameters:

    days: the number of days to query shootings for
    fatal: 0/1 indicating nonfatal vs fatal
    """

    # get the optional request args
    days = request.args.get("days", default=90, type=int)
    fatal = request.args.get("fatal", default=0, type=int)

    # create our SQL query
    query = (
        "SELECT * FROM shootings WHERE date_ >= current_date - %d AND fatal = %d"
        % (days, fatal)
    )

    # Query for the data
    URL = "https://phl.carto.com/api/v2/sql"
    WHERE = f"date_ >= current_date - {days} AND fatal = {fatal}"
    gdf = carto2gpd.get(URL, "shootings", where=WHERE)

    # count the number of fatal/non-fatal shootings
    count = (gdf["fatal"] == fatal).sum()

    # return the count
    if fatal == 1:
        return f"There have been {count} fatal shootings in the past {days} days"
    else:
        return f"There have been {count} nonfatal shootings in the past {days} days"


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)

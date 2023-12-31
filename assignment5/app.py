"""
The bridge between html and python.

Uses FastAPI to diplay HTML on local host in a
interactive way
"""
import datetime
from typing import List, Optional, Tuple
from fastapi.responses import HTMLResponse
import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    """
    Load the basepage when requested

    arguments:
    request(Request): Request to the server

    returns:
    templates.TemplateResponse with the 'strompris.html'
    template.
    """
    return templates.TemplateResponse("strompris.html",
    { "request": request,
      "location_codes": LOCATION_CODES,
      "today": datetime.date.today()
    })
@app.get('/plot_prices.json')
def strom_plot_json(
    locations: tuple = Query(default=tuple(LOCATION_CODES.keys())),
    end: datetime.date = datetime.date.today(),
    days: int = 7
):
    """
    Get strom price chart using strompris.py

    Is called whenever the strompris chart is loaded

    arguments:
    locations(tuple): The location codes for the
    locations to plot. Default is set to all locations.

    end(datetime.date): The latest date which to
    plot data for. Default set to today.

    days(int): The number of preceeding days from end
    which to plot. Default set to 7.

    returns:
    chart_dict(alt.Chart): chart with price plot as
    dictionary.

    """
    chart = plot_prices(fetch_prices(end, days, locations))
    chart_dict = alt.Chart.to_dict(chart)
    return chart_dict

app.mount(
path="/help",
app=StaticFiles(directory="docs/build/html"),
name="sphinx")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")

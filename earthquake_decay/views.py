# Views for earthquake_decay app
from django.shortcuts import render
from django.http import HttpResponse

import io
import csv
import json
from . import calculation
from django.views.decorators.csrf import csrf_exempt

def parse_event_data(file):
    """
    Parse uploaded file as a list of datetime.datetime objects.
    Accepts .csv/.txt with one datetime per row (YYYY-MM-DD HH:MM:SS).
    """
    import datetime as dt
    datetimes = []
    if hasattr(file, 'read'):
        file = io.TextIOWrapper(file, encoding='utf-8')
    reader = csv.reader(file)
    for row in reader:
        if not row:
            continue
        try:
            # Accept either a single string or two columns
            if len(row) == 1:
                dt_str = row[0].strip()
            else:
                dt_str = f"{row[0].strip()} {row[1].strip()}"
            datetimes.append(dt.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S'))
        except Exception:
            continue
    return datetimes

def build_plotly_data(bin_centers, frequencies, model_results, selected_models):
    import plotly.utils
    traces = [
        {
            'x': [str(calculation.mdates.num2date(x)) for x in bin_centers],
            'y': frequencies.tolist(),
            'mode': 'markers+lines',
            'name': 'Observed',
            'marker': {'color': 'red', 'symbol': 'star'},
            'line': {'dash': 'dot', 'color': 'red'},
        }
    ]
    model_colors = {
        'omori': 'blue', 'mogi1': 'orange', 'mogi2': 'green', 'utsu': 'purple'
    }
    for model in selected_models:
        res = model_results.get(model)
        if res and 'tt' in res and 'nt' in res:
            traces.append({
                'x': [str(calculation.mdates.num2date(x)) for x in bin_centers[:1] + list(res['tt'])],
                'y': [frequencies[0]] + res['nt'].tolist(),
                'mode': 'lines',
                'name': model.capitalize(),
                'line': {'color': model_colors.get(model, 'black')},
            })
    return json.dumps({
        'traces': traces,
        'xaxis_title': 'Time',
        'yaxis_title': 'Number of Earthquakes',
    }, cls=plotly.utils.PlotlyJSONEncoder)

def build_histogram_data(datetimes):
    import plotly.utils
    import numpy as np
    from matplotlib import dates as mdates
    if not datetimes:
        return None
    datnum = mdates.date2num(datetimes)
    counts, bins = np.histogram(datnum, bins=50)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    x = [str(mdates.num2date(b)) for b in bin_centers]
    y = counts.tolist()
    traces = [{
        'x': x,
        'y': y,
        'type': 'bar',
        'marker': {'color': 'rgba(100, 149, 237, 0.7)'},
        'name': 'Event Count',
    }]
    return json.dumps({
        'traces': traces,
        'xaxis_title': 'Date',
        'yaxis_title': 'Number of Events',
    }, cls=plotly.utils.PlotlyJSONEncoder)


def index(request):
    context = {}
    if request.method == 'POST':
        file = request.FILES.get('data_file')
        interval = float(request.POST.get('interval', 1))
        unit = request.POST.get('unit', 'Days')
        selected_models = request.POST.getlist('models')
        error = None
        datetimes = []
        if file:
            try:
                datetimes = parse_event_data(file)
            except Exception as e:
                error = f"Failed to parse file: {e}"
        if not datetimes:
            error = error or "No valid event data found. Please upload a .csv/.txt file with one datetime per row."
        if not error:
            try:
                results = calculation.run_earthquake_decay_models(datetimes, interval=interval, unit=unit, models=selected_models)
                context['plot_data'] = build_plotly_data(
                    results['bin_centers'], results['frequencies'], results, selected_models
                )
                context['histogram_data'] = build_histogram_data(datetimes)
                context['event_count'] = len(datetimes)
            except Exception as e:
                error = f"Calculation error: {e}"
        if error:
            context['error'] = error
    return render(request, 'earthquake_decay/earthquake_decay_analysis.html', context)

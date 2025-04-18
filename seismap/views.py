from django.views.generic import TemplateView
from django.shortcuts import redirect, render
import requests
from django.http import JsonResponse, HttpResponseServerError
import re
import io
import base64
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend for Matplotlib
import matplotlib.pyplot as plt
from obspy.imaging.beachball import beachball
import traceback # Import traceback
import os # Import os
import uuid # Import uuid
from django.conf import settings # Import settings

class SeismapView(TemplateView):
    template_name = 'seismap/seismap.html'
    context_object_name = 'seismap_view'

# Define a directory for temporary beachball images within MEDIA_ROOT
TEMP_BEACHBALL_DIR = os.path.join(settings.MEDIA_ROOT, 'seismap_temp')
# Ensure the directory exists
os.makedirs(TEMP_BEACHBALL_DIR, exist_ok=True)
# Define the corresponding URL path
TEMP_BEACHBALL_URL = os.path.join(settings.MEDIA_URL, 'seismap_temp').replace('\\', '/') # Ensure forward slashes for URL

# Function to parse Global CMT HTML data (Python version)
def parse_global_cmt_html(html_data):
    events = []
    # Split into blocks based on the HTML separator for events, skip header
    event_blocks = html_data.split('<hr><h3>Event name:')[1:]

    for block in event_blocks:
        event = {
            'cmtEventName': None, 'date': None, 'time': None, 'lat': None, 'lon': None,
            'depth': None, 'mb': None, 'ms': None, 'mw': None, 'region': None,
            'mt': None, 'exp': 0, 'beachball_img_url': None # Add field for image URL
        }

        try:
            # Extract Event Name
            match = re.match(r'^([^<]+)', block)
            if match: event['cmtEventName'] = match.group(1).strip()

            # Extract Region Name
            match = re.search(r'Region name:([^<]+)<br>', block)
            if match: event['region'] = match.group(1).strip()

            # Extract Date
            match = re.search(r'Date \(y/m/d\):\s*([\d/]+)', block)
            if match: event['date'] = match.group(1).replace('/', '-') # Format YYYY-MM-DD

            # Extract Timing info from <pre> block
            timing_pre_match = re.search(r'<b>Timing and location information</b>[\s\S]*?<pre>([\s\S]*?)</pre>', block)
            if timing_pre_match:
                timing_lines = timing_pre_match.group(1).strip().split('\n')
                for line in timing_lines:
                    trimmed_line = line.strip()
                    parts = trimmed_line.split()
                    if trimmed_line.startswith('PDEW') and len(parts) >= 8:
                        try: event['mb'] = float(parts[-2])
                        except ValueError: pass
                        try: event['ms'] = float(parts[-1])
                        except ValueError: pass
                    elif trimmed_line.startswith('CMT') and len(parts) >= 7:
                        try:
                            event['time'] = f"{parts[1]}:{parts[2]}:{parts[3]}"
                            event['lat'] = float(parts[4])
                            event['lon'] = float(parts[5])
                            event['depth'] = float(parts[6])
                        except (ValueError, IndexError): pass

            # Extract Mechanism info from <pre> block
            mechanism_pre_match = re.search(r'<b>Mechanism information</b>[\s\S]*?<pre>([\s\S]*?)</pre>', block)
            if mechanism_pre_match:
                mechanism_lines = mechanism_pre_match.group(1).strip().split('\n')
                for line in mechanism_lines:
                    trimmed_line = line.strip()
                    if trimmed_line.startswith('Exponent for moment tensor:'):
                        exp_match = re.search(r'Exponent for moment tensor:\s*(\d+)', trimmed_line)
                        if exp_match: event['exp'] = int(exp_match.group(1))
                    elif trimmed_line.startswith('CMT'):
                        mt_match = re.search(r'CMT\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', trimmed_line)
                        if mt_match:
                            try:
                                scale = 10**event['exp']
                                event['mt'] = [
                                    float(mt_match.group(1)) * scale, # Mrr
                                    float(mt_match.group(2)) * scale, # Mtt
                                    float(mt_match.group(3)) * scale, # Mpp
                                    float(mt_match.group(4)) * scale, # Mrt
                                    float(mt_match.group(5)) * scale, # Mrp
                                    float(mt_match.group(6)) * scale  # Mtp
                                ]
                            except ValueError: event['mt'] = None
                    elif trimmed_line.startswith('Mw ='):
                        mw_match = re.search(r'Mw =\s*([\d.]+)', trimmed_line)
                        if mw_match:
                            try: event['mw'] = float(mw_match.group(1))
                            except ValueError: pass

            # Generate beachball image if MT data is available
            if event.get('mt') and len(event['mt']) == 6:
                fig = None # Initialize fig to None
                try:
                    # Use ObsPy to generate the beachball figure
                    fig = plt.figure(figsize=(1, 1)) # Small figure size
                    ax = fig.add_subplot(111)
                    # Moment Tensor components for beachball: Mrr, Mtt, Mpp, Mrt, Mrp, Mtp
                    # Remove the unsupported 'axes' argument
                    beachball(event['mt'], size=100, linewidth=1, facecolor='black')
                    ax.set_axis_off() # Turn off axes
                    fig.tight_layout(pad=0) # Remove padding

                    # Generate unique filename
                    unique_id = uuid.uuid4()
                    filename = f"fm_{event['cmtEventName']}_{unique_id}.png"
                    filepath = os.path.join(TEMP_BEACHBALL_DIR, filename)
                    # Ensure URL uses forward slashes
                    file_url = f"{TEMP_BEACHBALL_URL}/{filename}".replace('\\', '/')

                    # Save the figure directly to the file
                    fig.savefig(filepath, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
                    plt.close(fig) # Close the figure to free memory

                    event['beachball_img_url'] = file_url # Store the URL

                except Exception as e:
                    print(f"Error generating beachball for {event.get('cmtEventName')}:")
                    traceback.print_exc() # Print the full traceback
                    event['beachball_img_url'] = None # Set URL to None if generation fails
                    if fig and plt.fignum_exists(fig.number):
                        plt.close(fig) # Ensure figure is closed even on error

            # Only add event if essential info was parsed
            if event.get('lat') is not None and event.get('lon') is not None:
                events.append(event)
            else:
                print(f"Warning: Failed to parse essential info for event: {event.get('cmtEventName')}")

        except Exception as parse_error:
            print(f"Error parsing HTML block for event: {parse_error}")
            # Optionally log the block content here for debugging

    return events


def fetch_cmt_data(request):
    base_url = "http://www.globalcmt.org/cgi-bin/globalcmt-cgi-bin/CMT5/form"
    # Extract parameters from request.GET, providing defaults if necessary
    params = {
        'itype': 'ymd',
        'yr': request.GET.get('yr', '1976'),
        'mo': request.GET.get('mo', '01'),
        'day': request.GET.get('day', '01'),
        'otype': 'ymd',
        'oyr': request.GET.get('oyr', '2025'), # Default to current year if needed
        'omo': request.GET.get('omo', '01'),
        'oday': request.GET.get('oday', '01'),
        'jyr': '1976', 'jday': '1', 'ojyr': '1976', 'ojday': '1',
        'nday': '1', 'lmw': request.GET.get('lmw', '0'), 'umw': request.GET.get('umw', '10'),
        'lms': '0', 'ums': '10', 'lmb': '0', 'umb': '10',
        'llat': request.GET.get('llat', '-90'), 'ulat': request.GET.get('ulat', '90'),
        'llon': request.GET.get('llon', '-180'), 'ulon': request.GET.get('ulon', '180'),
        'lhd': request.GET.get('lhd', '0'), 'uhd': request.GET.get('uhd', '1000'),
        'lts': '-9999', 'uts': '9999', 'lpe1': '0', 'upe1': '90',
        'lpe2': '0', 'upe2': '90', 'list': '5' # Use list format 5 (HTML)
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        # 'Accept': 'text/plain' # Keep trying text/plain, but parse HTML anyway
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status() # Raise an exception for bad status codes

        # Parse the HTML response using the Python function
        events_data = parse_global_cmt_html(response.text)

        return JsonResponse({'data': events_data}) # Return parsed data including images

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Global CMT: {e}")
        return JsonResponse({'error': f'Failed to fetch data from Global CMT: {e}'}, status=502) # Bad Gateway
    except Exception as e:
        print(f"An unexpected error occurred in fetch_cmt_data: {e}")
        # Consider logging the full traceback here
        return JsonResponse({'error': 'An internal server error occurred.'}, status=500)


def seismap_view(request):
    # Your view logic here, e.g., rendering the template
    return render(request, 'seismap/seismap.html')

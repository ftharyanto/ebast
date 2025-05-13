#!/usr/bin/env python
import os
import sys

def setup_django():
    # Add the project directory to the Python path
    project_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_path)
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebast.settings')
    import django
    django.setup()

def create_errorstation_table():
    from django.db import connection
    from django.db.utils import ProgrammingError
    
    # Get the ErrorStation model
    from qc.models import ErrorStation
    
    # Create the table if it doesn't exist
    try:
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ErrorStation)
        print("Successfully created ErrorStation table")
    except ProgrammingError as e:
        if 'already exists' in str(e):
            print("ErrorStation table already exists")
        else:
            raise

def update_station_coordinates():
    from cl_seiscomp.models import StationListModel
    
    # Dictionary of station codes with their corresponding latitude and longitude
    # Replace these with your actual station coordinates
    station_coordinates = {
        # Format: 'STATION_CODE': (latitude, longitude)
        # Example:
        # 'JAGI': (-7.6079, 112.9919),
        # 'VSI': (-7.9175, 112.5675),
        # Add more stations as needed
    }
    
    updated_count = 0
    
    for code, (lat, lon) in station_coordinates.items():
        try:
            station = StationListModel.objects.get(code=code)
            station.latitude = lat
            station.longitude = lon
            station.save()
            print(f"Updated coordinates for station {code}: {lat}, {lon}")
            updated_count += 1
        except StationListModel.DoesNotExist:
            print(f"Station {code} not found in the database")
        except Exception as e:
            print(f"Error updating station {code}: {str(e)}")
    
    print(f"\nUpdate complete. {updated_count} stations were updated.")

def main():
    setup_django()
    create_errorstation_table()
    
    print("\nWould you like to update station coordinates? (y/n): ")
    if input().lower() == 'y':
        update_station_coordinates()

if __name__ == "__main__":
    main()

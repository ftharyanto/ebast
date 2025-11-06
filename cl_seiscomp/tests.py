from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import StationListModel
from core.models import Operator
from django.contrib.auth.models import User
import io
import json


class StationListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('cl_seiscomp:station_list')
        
    def test_station_list_with_coordinates_shows_map(self):
        """Test that map is displayed when stations have coordinates"""
        # Create stations with coordinates
        StationListModel.objects.create(
            network='IA', code='JAGI', province='East Java', 
            location='Jajag', digitizer_type='Q330', UPT='BMKG Tretes',
            longitude=114.2266, latitude=-8.3264
        )
        StationListModel.objects.create(
            network='IA', code='VSI', province='East Java',
            location='Vesuvius', digitizer_type='Q330', UPT='BMKG Tretes',
            longitude=112.5675, latitude=-7.9175
        )
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['has_map_data'])
        self.assertIn('map_data', response.context)
        
        # Verify map data is valid JSON
        map_data = json.loads(response.context['map_data'])
        self.assertIn('data', map_data)
        self.assertIn('layout', map_data)
        
        # Verify station data in map
        scatter_data = map_data['data'][0]
        self.assertEqual(len(scatter_data['lat']), 2)
        self.assertEqual(len(scatter_data['lon']), 2)
        self.assertIn('JAGI', scatter_data['text'])
        self.assertIn('VSI', scatter_data['text'])
        
    def test_station_list_without_coordinates_no_map(self):
        """Test that map is not displayed when stations don't have coordinates"""
        # Create station without coordinates
        StationListModel.objects.create(
            network='IA', code='TEST', province='Test Province',
            location='Test Location', digitizer_type='Q330', UPT='Test UPT'
        )
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['has_map_data'])
        self.assertNotIn('map_data', response.context)
        
    def test_station_list_map_excludes_zero_coordinates(self):
        """Test that stations with 0,0 coordinates are excluded from map"""
        # Create station with valid coordinates
        StationListModel.objects.create(
            network='IA', code='VALID', province='East Java',
            location='Jajag', digitizer_type='Q330', UPT='BMKG Tretes',
            longitude=114.2266, latitude=-8.3264
        )
        # Create station with 0,0 coordinates (should be excluded)
        StationListModel.objects.create(
            network='IA', code='ZERO', province='Test',
            location='Test', digitizer_type='Q330', UPT='Test',
            longitude=0.0, latitude=0.0
        )
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['has_map_data'])
        
        # Verify only valid station is in map
        map_data = json.loads(response.context['map_data'])
        scatter_data = map_data['data'][0]
        self.assertEqual(len(scatter_data['lat']), 1)
        self.assertIn('VALID', scatter_data['text'])
        self.assertNotIn('ZERO', scatter_data['text'])


class StationBulkCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.operator = Operator.objects.create(name='Test Operator', NIP='1234567890')
        self.url = reverse('cl_seiscomp:sl_bulk_create')
        
    def test_valid_csv_file_upload(self):
        """Test successful bulk station creation with valid CSV file"""
        csv_content = b"network,code,province,location,digitizer_type,UPT,longitude,latitude\nNET1,ST01,Province1,Location1,Type1,UPT1,106.123,-6.456\nNET2,ST02,Province2,Location2,Type2,UPT2,107.789,-7.123"
        csv_file = SimpleUploadedFile("stations.csv", csv_content, content_type="text/csv")
        
        response = self.client.post(self.url, {'csv_file': csv_file})
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(StationListModel.objects.count(), 2)
        
        station1 = StationListModel.objects.get(code='ST01')
        self.assertEqual(station1.network, 'NET1')
        self.assertEqual(station1.longitude, 106.123)
        
    def test_valid_csv_data_paste(self):
        """Test successful bulk station creation with pasted CSV data"""
        csv_data = "NET1,ST01,Province1,Location1,Type1,UPT1,106.123,-6.456\nNET2,ST02,Province2,Location2,Type2,UPT2,107.789,-7.123"
        
        response = self.client.post(self.url, {'csv_data': csv_data})
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(StationListModel.objects.count(), 2)
        
    def test_invalid_longitude_latitude_types(self):
        """Test handling of invalid longitude/latitude data types"""
        csv_data = "NET1,ST01,Province1,Location1,Type1,UPT1,invalid_lon,invalid_lat"
        
        response = self.client.post(self.url, {'csv_data': csv_data})
        
        # Should handle error gracefully, not return 500
        self.assertNotEqual(response.status_code, 500)
        self.assertEqual(StationListModel.objects.count(), 0)
        
    def test_missing_csv_columns(self):
        """Test handling of CSV rows with missing columns"""
        csv_data = "NET1,ST01,Province1"  # Missing 5 columns
        
        response = self.client.post(self.url, {'csv_data': csv_data})
        
        # Should handle error gracefully, not return 500
        self.assertNotEqual(response.status_code, 500)
        self.assertEqual(StationListModel.objects.count(), 0)
        
    def test_empty_csv_rows(self):
        """Test handling of empty CSV rows"""
        csv_data = "NET1,ST01,Province1,Location1,Type1,UPT1,106.123,-6.456\n\n\nNET2,ST02,Province2,Location2,Type2,UPT2,107.789,-7.123"
        
        response = self.client.post(self.url, {'csv_data': csv_data})
        
        # Should handle empty rows gracefully
        self.assertNotEqual(response.status_code, 500)
        self.assertEqual(StationListModel.objects.count(), 2)
        
    def test_no_csv_file_or_data(self):
        """Test error handling when no CSV file or data is provided"""
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, 302)  # Redirect with error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Please upload a CSV file or provide CSV data' in str(m) for m in messages))
        
    def test_invalid_file_extension(self):
        """Test error handling for non-CSV files"""
        txt_file = SimpleUploadedFile("stations.txt", b"some content", content_type="text/plain")
        
        response = self.client.post(self.url, {'csv_file': txt_file})
        
        self.assertEqual(response.status_code, 302)  # Redirect with error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('This is not a CSV file' in str(m) for m in messages))

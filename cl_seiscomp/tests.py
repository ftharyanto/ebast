from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import StationListModel
from core.models import Operator
from django.contrib.auth.models import User
import io


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

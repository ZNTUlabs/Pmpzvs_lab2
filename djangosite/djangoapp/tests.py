from django.urls import reverse_lazy
from django.test import TestCase
from django.http import HttpResponseNotAllowed
from .models import Measurement



class TestCalls(TestCase):
    def setUp(self):
        self.create_url = 'create_measurement'
        self.list_url = 'measurement_list'
        
    def test_call_view_loads(self):
        for url in [self.create_url, self.list_url]:
            path = str(reverse_lazy(url))
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, '{}.html'.format(url))

    def test_call_view_fails_blank(self):
        path = str(reverse_lazy(self.create_url))
        response = self.client.post(path, {})
        self.assertFormError(response, 'form', 'value', u'This field is required.')

    def test_call_view_fails_incorrect(self):
        path = str(reverse_lazy(self.create_url))
        value = '1'*51
        measurement_params = {'value': value,}
        response = self.client.post(path, measurement_params)
        self.assertFormError(response, 'form', 'value', u'Ensure this value has at most 50 characters (it has 51).')

    def test_call_view_succeed(self):
        path = str(reverse_lazy(self.create_url))
        value = '1'*10
        description = 'measurement description'
        measurement_params = {'value': value, 'description': description}
        response = self.client.post(path, measurement_params)
        self.assertEqual(response.status_code, 302)
        measurement = Measurement.objects.get(id=1)
        for field in measurement_params.keys():
            measurement_field = getattr(measurement, field)
            self.assertEqual(measurement_field, measurement_params[field])

from django.shortcuts import render

import os
from django.views import generic
from django.conf import settings
from djangoapp.models import Measurement
from django.urls import reverse_lazy
from djangoapp.forms import MeasurementForm

class MeasurementList(generic.ListView):
    model = Measurement
    context_object_name = 'measurements'
    template_name = 'measurement_list.html'

    def get(self, request, *args, **kwargs):
        try:
            file_path = os.path.join(settings.BASE_DIR, 'measurement/mesurement.log')
            measurement_file = open(file_path, 'r')
            for value in measurement_file:
                Measurement.objects.get_or_create(value=value)
        except IOError:
            pass
        return super(MeasurementList, self).get(request, *args, **kwargs)

class MeasurementCreate(generic.CreateView):
    form_class = MeasurementForm
    template_name = 'create_measurement.html'
    success_url = reverse_lazy('measurement_list')

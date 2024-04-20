from django import forms
from department.models import BedModel
from .models import OccupyWardModel
from django.forms.widgets import DateInput
import datetime
from datetime import datetime, timedelta
from django.utils import timezone


class OccupyWardForm(forms.ModelForm):
    date_checkin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_checkout = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = OccupyWardModel
        fields = ['full_name', 'telephone', 'bed', 'date_checkin', 'date_checkout', 'comment', 'operation', 'color']

    def __init__(self, *args, **kwargs):
        ward_slug = kwargs.pop('ward_slug', None)
        super(OccupyWardForm, self).__init__(*args, **kwargs)
        if ward_slug:
            self.fields['bed'].queryset = BedModel.objects.filter(ward__slug=ward_slug)
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
        user = kwargs.pop('user', None)
        ward_slug = kwargs.pop('ward_slug', None)
        super(OccupyWardForm, self).__init__(*args, **kwargs)

        if ward_slug and user:
            self.fields['bed'].queryset = BedModel.objects.filter(
                ward__department__slug=user.department.slug
            )
        
    def clean(self):
        cleaned_data = super().clean()
        date_checkin = cleaned_data.get("date_checkin")
        date_checkout = cleaned_data.get("date_checkout")
        
        if date_checkout and date_checkin and date_checkout <= date_checkin:
            raise forms.ValidationError("Дата выезда должна быть позже даты заезда!")
        
        if date_checkin and date_checkout:
            days_range = [date_checkin + timedelta(days=i) for i in range(1, (date_checkout - date_checkin).days)]
            
            for day in days_range:
                if OccupyWardModel.objects.filter(bed=cleaned_data['bed'], date_checkin=day).exists():
                    patient = OccupyWardModel.objects.get(bed=cleaned_data['bed'], date_checkin=day).full_name
                    raise forms.ValidationError(f"Койка уже занята на дату {day} пациентом {patient}")
        
        return cleaned_data
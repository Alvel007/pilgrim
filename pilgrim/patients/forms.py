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
        bed = cleaned_data.get('bed')
        date_checkin = cleaned_data.get('date_checkin')
        date_checkout = cleaned_data.get('date_checkout')

        if date_checkin and date_checkout:
            if date_checkin >= date_checkout:
                raise forms.ValidationError("Дата заезда должна быть раньше даты выезда.")

            # Проверяем, что койка не занята в период с date_checkin (не включая) по date_checkout (не включая)
            conflicting_reservations = OccupyWardModel.objects.filter(
                bed=bed,
                date_checkout__gt=date_checkin,
                date_checkin__lt=date_checkout
            )
            if conflicting_reservations.exists():
                names = ', '.join([reservation.full_name for reservation in conflicting_reservations])
                raise forms.ValidationError(f"{bed} уже занята в этот период другими пациентами: {names}.")

        return cleaned_data
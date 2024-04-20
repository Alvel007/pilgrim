from django.views.generic import ListView

from django.db.models import Q
from datetime import datetime, timedelta
from calendar import monthrange
from django.utils import timezone

from datetime import date
from calendar import HTMLCalendar
from django import template
import calendar
from collections import defaultdict
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from patients.models import OccupyWardModel
from department.models import DepartmentModel, BedModel, WardModel

from django.urls import reverse
from patients.forms import OccupyWardForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, reverse

from .forms import CustomAuthenticationForm

register = template.Library()

MONTH_NAMES = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}

MONTH_NAMES_RP = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}

def home_view(request):
    departments = DepartmentModel.objects.all()
    current_time = datetime.now()
    year = current_time.year
    month = current_time.month
    return render(request, 'home.html', {'departments': departments, 'year': year, 'month': month})

class AccountBedsView(ListView):  
    model = WardModel  
    template_name = 'account_beds.html'  
    context_object_name = 'wards'  
    def get_queryset(self):  
        department_slug = self.kwargs.get('department_slug')  
        department = DepartmentModel.objects.get(slug=department_slug)  
        queryset = WardModel.objects.filter(department=department)  
        return queryset  
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            

            context['department_slug'] = self.kwargs.get('department_slug')
            context['year'] = int(self.kwargs.get('year'))
            context['month'] = int(self.kwargs.get('month'))

            department_slug = self.kwargs.get('department_slug')
            department = DepartmentModel.objects.get(slug=department_slug)

            wards = self.get_queryset().filter(department=department)
            context['wards'] = wards
            context['department'] = department


            year = int(self.kwargs.get('year'))
            month = int(self.kwargs.get('month'))
            previous_month = month
            next_month = month
            if month == 1:
                previous_month = 12
                previous_year = year - 1
            else:
                previous_month -= 1
                previous_year = year
            if month == 12:
                next_month = 1
                next_year = year + 1
            else:
                next_month += 1
                next_year = year
            context['previous_month'] = previous_month
            context['previous_year'] = previous_year
            context['next_month'] = next_month
            context['next_year'] = next_year


            month_name = MONTH_NAMES.get(month)
            context['month_name'] = month_name

            year = int(self.kwargs.get('year'))
            month = int(self.kwargs.get('month'))
            _, num_days = calendar.monthrange(year, month)
            days_with_markings = {day: 'Weekend' if idx % 7 in [5, 6] else 'Weekday' for idx, day in enumerate(range(1, num_days + 1))}

            occupancy_data = []
            for ward in wards:
                for bed in ward.bedmodel_set.all():
                    bed_data = {
                        'ward': ward.name,
                        'number': bed.number,
                        'department': bed.ward.department.name,
                        'occupancy': [
                            {
                                'day': day,
                                'occupied': False,
                                'first_day': False,
                                'last_day': False,
                                'operation': False,
                                'color': '#9fb5ffc4' if calendar.weekday(year, month, day) in [5, 6] else '#FFFFFF',  # Change color based on weekday
                                'prev_color': '#FFFFFF'
                            } for day in range(1, num_days + 1)
                        ]
                    }
                    occupancy_data.append(bed_data)

            bookings = OccupyWardModel.objects.order_by('date_checkin').filter(Q(date_checkin__lte=datetime(year, month, num_days)) & Q(date_checkout__gte=datetime(year, month, 1)))

            for booking in bookings:
                current_date = booking.date_checkin
                while current_date <= booking.date_checkout:
                    if current_date.month == month:
                        for bed_data in occupancy_data:
                            if bed_data['ward'] == booking.bed.ward.name and bed_data['number'] == booking.bed.number and bed_data['department'] == booking.bed.ward.department.name:
                                day_data = next((day for day in bed_data['occupancy'] if day['day'] == current_date.day), None)
                                if day_data:
                                    day_data['occupied'] = True
                                    if current_date == booking.date_checkin:
                                        day_data['first_day'] = True
                                    if current_date == booking.date_checkout:
                                        day_data['last_day'] = True
                                    day_data['operation'] = booking.operation
                                    day_data['color'] = booking.color
                                    day_data['ward_slug'] = booking.bed.ward.slug
                                    day_data['bed_slug'] = booking.bed.slug
                                    day_data['prev_color'] = bed_data['occupancy'][current_date.day - 2]['color'] if current_date.day > 1 else '#FFFFFF'
                    current_date += timezone.timedelta(days=1)

            context['num_days'] = num_days + 1
            context['days_with_markings'] = days_with_markings
            context['occupancy_data'] = occupancy_data
            return context
    

    def get_next_month(self):
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        return year, month


def create_occupy_ward(request, department_slug, ward_slug, bed_slug, year, month, day):
    bed = BedModel.objects.get(slug=bed_slug)
    user = request.user
    date_checkin = datetime(year, month, day).date()
    date_checkout = date_checkin + timedelta(days=3)

    if request.method == 'POST':
        form = OccupyWardForm(request.POST)
        if form.is_valid():
            if user.department.slug == bed.ward.department.slug:
                form.save()
                return redirect('account_beds', department_slug=department_slug, year=year, month=month)
            else:
                return redirect('error_page')
    else:
        initial_data = {
            'bed': bed.id,
            'date_checkin': date_checkin.strftime('%Y-%m-%d'),
            'date_checkout': date_checkout.strftime('%Y-%m-%d')
        }
        form = OccupyWardForm(initial=initial_data)

    context = {
        'form': form,
        'department_slug': department_slug,
        'ward_slug': ward_slug,
        'bed_slug': bed_slug,
        'year': year,
        'month': month,
        'day': day
    }
    return render(request, 'create_occupy_ward.html', context)

def day_info(request, department_slug, ward_slug, bed_slug, year, month, day):
    date = datetime(year, month, day)
    occupy_instances = OccupyWardModel.objects.filter(
        bed__ward__department__slug=department_slug,
        bed__ward__slug=ward_slug,
        bed__slug=bed_slug,
        date_checkin__lte=date,
        date_checkout__gte=date)
    
    if occupy_instances.count() == 1:
        first_instance = occupy_instances.first()
        second_instance = None
    elif occupy_instances.count() > 1:
        first_instance = occupy_instances[0]
        second_instance = occupy_instances[1]
    else:
        first_instance = None
        second_instance = None
    
    current_bed = BedModel.objects.get(ward__department__slug=department_slug, ward__slug=ward_slug, slug=bed_slug)
    formatted_date = f"{day} {MONTH_NAMES_RP[month]} {year} года"

    context = {
        'first_instance': first_instance,
        'second_instance': second_instance,
        'current_bed': current_bed,
        'formatted_date': formatted_date,
    }
    
    return render(request, 'day_info_occupy_ward.html', context)


@login_required
def delete_occupy_instance(request, pk):
    instance = get_object_or_404(OccupyWardModel, pk=pk)
    user = request.user
    if user.department.slug == instance.bed.ward.department.slug:
        department_slug = instance.bed.ward.department.slug
        year = instance.date_checkin.year
        month = instance.date_checkin.month
        instance.delete()
        redirect_url = reverse('account_beds', args=[department_slug, year, month])
        return redirect(redirect_url)
    else:
        return redirect('error_page')


@login_required
def edit_occupy_ward(request, pk):
    occupy_instance = OccupyWardModel.objects.get(id=pk)
    date_checkin = occupy_instance.date_checkin
    date_checkout = occupy_instance.date_checkout
    department_slug = occupy_instance.bed.ward.department.slug
    year = occupy_instance.date_checkin.year
    month = occupy_instance.date_checkin.month
    user = request.user

    if request.method == 'POST':
        form = OccupyWardForm(request.POST, instance=occupy_instance)
        if form.is_valid():
            if user.department.slug == occupy_instance.bed.ward.department.slug:
                form.save()
                return redirect('account_beds', department_slug=occupy_instance.bed.ward.department.slug, year=occupy_instance.date_checkin.year, month=occupy_instance.date_checkin.month)
            else:
                return redirect('error_page')
    else:
        initial_data = {
            'bed': occupy_instance.bed.id,
            'date_checkin': date_checkin.strftime('%Y-%m-%d'),
            'date_checkout': date_checkout.strftime('%Y-%m-%d')
        }
        form = OccupyWardForm(initial=initial_data, instance=occupy_instance)

    context = {
        'form': form,
        'occupy_id': pk, 
        'department_slug': department_slug,
        'year': year,
        'month': month
    }
    return render(request, 'edit_occupy_ward.html', context)


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                department_slug = user.department.slug
                current_time = datetime.now()
                year = current_time.year
                month = current_time.month
                response = redirect('account_beds', department_slug=department_slug, year=year, month=month)
                response['Cache-Control'] = 'no-store'
                return response
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('home'))


def error_page(request):
    return render(request, 'error_page.html')
from django.contrib import admin
from django.urls import path
from .views import home_view, AccountBedsView, create_occupy_ward, day_info, delete_occupy_instance, edit_occupy_ward, logout_view, login_view, error_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home',),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<str:department_slug>/<int:year>/<int:month>/', AccountBedsView.as_view(), name='account_beds'),
    path('<str:department_slug>/<str:ward_slug>/<str:bed_slug>/<int:year>/<int:month>/<int:day>/', day_info, name='day_info'),
    path('<str:department_slug>/<str:ward_slug>/<str:bed_slug>/<int:year>/<int:month>/<int:day>/create_occupy_ward/', create_occupy_ward, name='create_occupy_ward'),
    path('edit-occupy-ward/<int:pk>/', edit_occupy_ward, name='edit_occupy_ward'),
    path('delete/<int:pk>/', delete_occupy_instance, name='delete_occupy_instance'),
    path('error/', error_page, name='error_page'),
]
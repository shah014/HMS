import django_filters
from .models import *
from django_filters import DateFilter


class PatientFiter(django_filters.FilterSet):
    start_date = DateFilter(field_name="Created_at", lookup_expr='gte')
    end_date = DateFilter(field_name="Created_at", lookup_expr='lte')

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['address', 'age', 'bloodGroup', 'email', 'contact', 'symptoms',
                   'Created_at', 'name', 'profile_pic']


class Doctorfilter(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ['address', 'contact', 'profile_pic']


# class AppointmentFilter(django_filters.FilterSet):
#     class Meta:
#         model = Appointment
#         fileds = '__all__'
#         exclude = ['doctor']


class AvailableBedFilter(django_filters.FilterSet):
    class Meta:
        model = Hospital
        fields = '__all__'
        exclude = ['ICU', 'HDU', 'ventilator', 'email', 'contact']

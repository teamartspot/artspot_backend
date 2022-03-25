import django_filters

from .models import User

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
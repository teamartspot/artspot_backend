from django.db.models.query import QuerySet
from typing import List

from .models import User
#from .filters import UserFilter

#Returns the user list with fields defined in the filter for each user
def get_users(*, filters=None) -> List[User]:
    filters = filters or {}
    qs = User.objects.all()
    list_qs = list(qs.values('email', 'last_name', 'first_name'))
    return (list_qs)

def get_user_from_email(*, email = None) -> User:
    user = User.objects.get(email__exact = email)
    return user
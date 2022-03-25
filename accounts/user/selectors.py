from django.db.models.query import QuerySet

from .models import User
#from .filters import UserFilter

#Returns the user list with fields defined in the filter for each user
def get_users(*, filters=None) -> QuerySet[User]:
    filters = filters or {}
    qs = User.objects.all()
    return qs
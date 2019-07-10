from django.urls import path
from django.urls import include
from .views import *


urlpatterns = [
    path('', faculty_list),
    path('<faculty>', group_choise),
    path('<faculty>/<group>', group_schedule)
]

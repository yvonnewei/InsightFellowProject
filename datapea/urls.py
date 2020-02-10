from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from datapea import views


# API endpoints
urlpatterns = format_suffix_patterns([
    # path('', views.api_root),
    path('', views.Home.as_view(), name='home'),
    path('patients/',
         views.PatientList.as_view(),
         name='patient-list'),
    path('patients/<int:pk>/',
         views.PatientDetail.as_view(),
         name='patient-detail'),

    path('providers/',
         views.UserList.as_view(),
         name='user-list'),
    path('providers/<int:pk>/',
         views.UserDetail.as_view(),
         name='user-detail')
])

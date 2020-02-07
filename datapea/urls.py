from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from datapea import views
# from datapea.views import PatientViewSet, UserViewSet
# from datapea.views import api_root
from rest_framework import renderers

#
# urlpatterns = [
#     path('', views.api_root),
#     # path('providers/', views.provider_list.as_view()),
#     # path('providers/<int:pk>/', views.provider_detail.as_view()),
#     path('patients/', views.patient_list.as_view()),
#     path('patients/<int:pk>/', views.patient_detail.as_view()),
#     # path('drugs/', views.drug_list.as_view()),
#     # path('drugs/<int:pk>/', views.drug_list.as_view()),
#     path('users/', views.UserList.as_view()),
#     path('users/<int:pk>/', views.UserDetail.as_view()),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)

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

# Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'patients', views.PatientViewSet)
# router.register(r'providers', views.UserViewSet)
#
# # The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
# ]
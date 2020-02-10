# /////////////////////////////////////////////////////////////
import requests
from django.contrib.auth import authenticate, login
from django.http import  HttpResponseRedirect
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer

from datapea.models import Patient
from datapea.permissions import IsOwnerOrReadOnly, OnlyOwnerReadOnly
from datapea.serializers import PatientSerializer, UserSerializer

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes

from rest_framework.response import Response
from django.shortcuts import render, redirect

ADMIN_AUTH = ('admin', 'password')
STAFF = ('staff1', 'chrdwhdhxt')


class Home(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

    def post(self, request):
        user = {}
        print ("request post: {}".format(request.POST))
        if request.POST.get('patient_id'):
            username = request.POST.get('patient_id')
            role = request.POST.get('role')
            print("username: {}".format(username))
            print("role: {}".format(role))
            #url = 'http://www.datapea.me/patients/{}'.format(username)
            url = '/patients/{}'.format(username)
            print("url: {}".format(url))
            if role == 'Admin':
                user = authenticate(username='admin', password='password')
            else:
                user = authenticate(username='staff1', password='chrdwhdhxt')
            print('user: {}'.format(user))
            if user:
            	login(request, user)
            	auth = ADMIN_AUTH if role == 'Admin' else STAFF
            	return HttpResponseRedirect(url)

        return render(request, 'home.html')


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):

    serializer_class = UserSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_detail.html'

    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(pk=kwargs['pk'])
        print(queryset)
        return Response({'users': queryset})

@permission_classes([IsAuthenticatedOrReadOnly])
class PatientList(generics.ListCreateAPIView):
    """
           List all patients, or create a new patient.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)


@permission_classes([IsAuthenticated & OnlyOwnerReadOnly])
class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    """
            Retrieve, update or delete a patient.
    """
    # queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'patient_detail.html'

    def get(self, request, *args, **kwargs):
        queryset = Patient.objects.filter(pk=kwargs['pk'])
        self.check_object_permissions(request, queryset.first())
        return Response({'patients': queryset})

    def post(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        serializer = PatientSerializer(patient, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'patient': patient})
        serializer.save()
        return redirect('patient_list')

# ////////////////////////
# keep this
# class PatientViewSet(viewsets.ModelViewSet):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#     #                       IsOwnerOrReadOnly]
#     permission_classes = [permissions.IsAuthenticated,
#                           OnlyOwnerReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(provider=self.request.user)
# /////////////////////////////////////////////////////////////

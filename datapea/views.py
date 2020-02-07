# /////////////////////////////////////////////////////////////
import requests
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from rest_framework import generics, renderers
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer, JSONRenderer

from datapea.models import Patient
from datapea.permissions import IsOwnerOrReadOnly, OnlyOwnerReadOnly
from datapea.serializers import PatientSerializer, UserSerializer

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
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
            	#response = requests.get(url, auth=auth)
            	#if response.status_code == 200:
            	return HttpResponseRedirect(url)
            	#print("response: {}".format(response))
            	#if response.status_code == 403:
            		#raise PermissionDenied
        # return render(request, 'home.html', {'user': user})
        return render(request, 'home.html')

#
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'providers': reverse('user-list', request=request, format=format),
#         'patients': reverse('patient-list', request=request, format=format)
#     })


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


# ////////
# keep this
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# //////
#
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

# from rest_framework import generics
# from datapea.models import Provider, Patient, Drug
# from datapea.permissions import IsOwnerOrReadOnly
# from datapea.serializers import ProviderSerializer, PatientSerializer, DrugSerializer
# from rest_framework import permissions
#
#
# # Create your views here.
# class provider_list(generics.ListCreateAPIView):
#     """
#            List all providers, or create a new provider.
#     """
#     queryset = Provider.objects.all()
#     serializer_class = ProviderSerializer
#
#
# class provider_detail(generics.RetrieveUpdateDestroyAPIView):
#     """
#         Retrieve, update or delete a provider.
#     """
#     queryset = Provider.objects.all()
#     serializer_class = ProviderSerializer
#
#
# class patient_list(generics.ListCreateAPIView):
#     """
#            List all patients, or create a new patient.
#     """
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
#
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(provider=self.request.pk)
#
#
# class patient_detail(generics.RetrieveUpdateDestroyAPIView):
#     """
#             Retrieve, update or delete a patient.
#     """
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]
#
#
# class drug_list(generics.ListCreateAPIView):
#     """
#          List all drugs, or create a new drug.
#     """
#     queryset = Drug.objects.all()
#     serializer_class = DrugSerializer
#
#
# class drug_detail(generics.RetrieveUpdateDestroyAPIView):
#     """
#             Retrieve, update or delete a drug.
#     """
#     queryset = Drug.objects.all()
#     serializer_class = DrugSerializer
#
# # def provider_list(APIView):
# #
# #
# #     def get(self, request, format=None):
# #         providers = Provider.objects.all()
# #         serializer = ProviderSerializer(providers, many=True)
# #         return Response(serializer.data)
# #
# #     def post(self, request, format=None):
# #         serializer = ProviderSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # def provider_detail(APIView):
# #
# #
# #     def get_object(self, pk):
# #         try:
# #             return Provider.objects.get(pk=pk)
# #         except Provider.DoesNotExist:
# #             raise Http404
# #
# #     def get(self, request, pk, format=None):
# #         provider = self.get_object(pk)
# #         serializer = ProviderSerializer(provider)
# #         return Response(serializer.data)
# #
# #     def put(self, request, pk, format=None):
# #         provider = self.get_object(pk)
# #         serializer = ProviderSerializer(provider, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def delete(self, request, pk, format=None):
# #         provider = self.get_object(pk)
# #         provider.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# # @api_view(['GET', 'POST'])
# # def patient_list(request):
# #     """
# #            List all patients, or create a new patient.
# #     """
# #     if request.method == 'GET':
# #         patients = Patient.objects.all()
# #         serializer = PatientSerializer(patients, many=True)
# #         return Response(serializer.data)
# #     elif request.method == 'POST':
# #         serializer = PatientSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # @api_view(['GET', 'PUT', 'DELETE'])
# # def patient_detail(request, pk):
# #     """
# #             Retrieve, update or delete a patient.
# #     """
# #     try:
# #         patient = Patient.objects.get(pk=pk)
# #     except Patient.DoesNotExist:
# #         return Response(status=status.HTTP_404_NOT_FOUND)
# #
# #     if request.method == 'GET':
# #         serializer = PatientSerializer(patient)
# #         return Response(serializer.data)
# #
# #     elif request.method == 'PUT':
# #         serializer = PatientSerializer(patient, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     elif request.method == 'DELETE':
# #         patient.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
#
# #
# # @api_view(['GET', 'POST'])
# # def drug_list(request):
# #     """
# #          List all drugs, or create a new drug.
# #     """
# #     if request.method == 'GET':
# #         drugs = Drug.objects.all()
# #         serializer = DrugSerializer(drugs, many=True)
# #         return Response(serializer.data)
# #     elif request.method == 'POST':
# #         serializer = DrugSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # @api_view(['GET', 'PUT', 'DELETE'])
# # def provider_detail(request, pk):
# #     """
# #             Retrieve, update or delete a drug.
# #     """
# #     try:
# #         drug = Drug.objects.get(pk=pk)
# #     except Drug.DoesNotExist:
# #         return Response(status=status.HTTP_404_NOT_FOUND)
# #
# #     if request.method == 'GET':
# #         serializer = DrugSerializer(drug)
# #         return Response(serializer.data)
# #
# #     elif request.method == 'PUT':
# #         serializer = DrugSerializer(drug, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     elif request.method == 'DELETE':
# #         drug.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)

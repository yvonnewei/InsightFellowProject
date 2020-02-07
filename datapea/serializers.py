from django.contrib.auth.models import User
from rest_framework import serializers

# from datapea.models import Provider, Patient, Drug
# /////////////////////////////////////////////////////////////

from datapea.models import Patient
from django.contrib.auth.models import User


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    provider = serializers.ReadOnlyField(source='provider.username')

    class Meta:
        model = Patient
        # fields = '__all__'
        fields = ['url',
                  'id',
                  'last_name',
                  'first_name',
                  'insurance',
                  'address',
                  'date_of_birth',
                  'gender',
                  'phone',
                  'ssn',
                  'provider']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # patients = serializers.PrimaryKeyRelatedField(many=True, queryset=Patient.objects.all())
    patients = serializers.HyperlinkedRelatedField(many=True, view_name='patient-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'patients']

# /////////////////////////////////////////////////////////////
# class ProviderSerializer(serializers.ModelSerializer):
#
#     patients = serializers.PrimaryKeyRelatedField(many=True, queryset=Patient.objects.all())
#
#     class Meta:
#         model = Provider
#         # model = User
#         # fields = '__all__'
#         fields = ['pk',
#                   'national_provider_identifier',
#                   'last_name',
#                   'first_name',
#                   'city',
#                   'state',
#                   'specialty_description',
#                   'source_of_provider_specialty',
#                   'patients']
#
#
# class PatientSerializer(serializers.HyperlinkedModelSerializer):
#
#     provider = serializers.ReadOnlyField(source='provider.pk')
#
#     class Meta:
#         model = Patient
#         # fields = '__all__'
#         fields = ['pk',
#                   'last_name',
#                   'first_name',
#                   'insurance',
#                   'address',
#                   'date_of_birth',
#                   'gender',
#                   'phone',
#                   'ssn',
#                   'provider']
#
#
# class DrugSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Drug
#         # fields = '__all__'
#         fields = ['pk',
#                   'drug_name',
#                   'generic_name']

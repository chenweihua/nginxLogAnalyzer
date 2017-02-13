from rest_framework import serializers
from application.models import vrijeme_promet, overall, ipcontent, Requests_vrijeme, Status, Najaktivniji, Contents, status_per_hour206, status_per_hour200, status_per_hour404, status_per_hour301, status_per_hour302, status_per_hour403, status_per_hour405, status_per_hour406, status_per_hour500, status_per_hour504
from django.utils import timezone


class VrijemePrometSerializer(serializers.ModelSerializer):
    class Meta:
        model = vrijeme_promet
        fields = ['id', 'vrijeme', 'promet']

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests_vrijeme
        fields = ['id', 'vrijeme', 'requests']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'status', 'brojponavljanja']

class NajaktivnijiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Najaktivniji
        fields = ['id', 'ip', 'brojponavljanja']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = ['id', 'content', 'brojponavljanja']


class CodeSerializer200(serializers.ModelSerializer):
   
    class Meta:
        model = status_per_hour200
        fields = ['id', 'time', 'y']


class CodeSerializer206(serializers.ModelSerializer):
    
    class Meta:
        model = status_per_hour206
        fields = ['id', 'time', 'y']
        

class CodeSerializer404(serializers.ModelSerializer):
    
    class Meta:
        model = status_per_hour404
        fields = ['id', 'time', 'y']
 

class CodeSerializer301(serializers.ModelSerializer):

    class Meta:
        model = status_per_hour301
        fields = ['id', 'time', 'y']

class CodeSerializer302(serializers.ModelSerializer):

    class Meta:
        model = status_per_hour302
        fields = ['id', 'time', 'y']

class CodeSerializer403(serializers.ModelSerializer):

    class Meta:
        model = status_per_hour403
        fields = ['id', 'time', 'y']

class CodeSerializer405(serializers.ModelSerializer):

    class Meta:
        model = status_per_hour405
        fields = ['id', 'time', 'y']

class CodeSerializer406(serializers.ModelSerializer):

    class Meta:
        model = status_per_hour406
        fields = ['id', 'time', 'y']


class CodeSerializer500(serializers.ModelSerializer):

    class Meta:
        model = status_per_hour500
        fields = ['id', 'time', 'y']


class CodeSerializer504(serializers.ModelSerializer):

    class Meta:
        model = status_per_hour504
        fields = ['id', 'time', 'y']

class IpcontentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ipcontent
        fields = ['id', 'ip', 'content', 'counts']

class OverallSerializer(serializers.ModelSerializer):

    class Meta:
        model = ipcontent
        fields = ['id', 'promet', 'code200', 'code404', 'ip', 'content', 'fajl', 'code', 'total', 'metod', 'status400', 'status403']
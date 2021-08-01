from rest_framework import serializers
from .models import Algorithm

class AlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ('id', 'title', 'description', 'unitsize', 'width', 'height', 'sievesize', 'minimumradius', 'finerpercent', 'voidratio', 'cellsize', 'density')
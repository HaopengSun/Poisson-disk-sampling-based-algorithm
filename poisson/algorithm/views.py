from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AlgorithmSerializer
from .models import Algorithm

# Create your views here.

class AlgorithmView(viewsets.ModelViewSet):
    serializer_class = AlgorithmSerializer
    queryset = Algorithm.objects.all()
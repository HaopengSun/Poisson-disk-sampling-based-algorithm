from django.contrib import admin
from .models import Algorithm

class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'unitsize', 'width', 'height', 'sievesize')

admin.site.register(Algorithm, AlgorithmAdmin)

from rest_framework import viewsets
from .models import Study, Assay
from .serializers import StudySerializer, AssaySerializer

class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

class AssayViewSet(viewsets.ModelViewSet):
    queryset = Assay.objects.all()
    serializer_class = AssaySerializer
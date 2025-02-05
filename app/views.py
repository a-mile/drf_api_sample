from .apiutils import APIUtilsViewSet
from .models import Assay, Study
from .serializers import AssaySerializer, StudySerializer


class StudyViewSet(APIUtilsViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer


class AssayViewSet(APIUtilsViewSet):
    queryset = Assay.objects.all()
    serializer_class = AssaySerializer

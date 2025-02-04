from rest_framework import serializers
from .models import Study, Assay


class AssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assay
        fields = ["id", "measurement_type", "study"]

class StudySerializer(serializers.ModelSerializer):
    assays = AssaySerializer(many=True, read_only=True)
    class Meta:
        model = Study
        fields = ["id", "title", "description", "assays"]
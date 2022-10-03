from rest_framework import serializers
from .models import userprofile


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = userprofile
        fields = [
            "sr_name",
            "work_stream",
            "work_stream",
            "task",
            "value_hml",
            "urgent_yn",
            "request_date",
            "needed_date",
            "etd",
        ]

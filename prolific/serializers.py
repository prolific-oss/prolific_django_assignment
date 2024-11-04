from rest_framework import serializers
from prolific import constants
from prolific.exceptions import StudyCompletedError
from prolific.models import Study, Submission


class StudySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=200)
    total_places = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    status = serializers.CharField(required=False, max_length=20, read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Study` instance, given the validated data.
        """
        return Study.objects.create(**validated_data)


class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    study_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    started_at = serializers.DateTimeField(required=False, read_only=True)
    completed_at = serializers.DateTimeField(required=False, read_only=True)
    status = serializers.CharField(required=False, max_length=20)

    def validate_study_id(self, study_id):
        study = Study.objects.get(id=study_id)
        if study.status == constants.STATUS_COMPLETED:
            raise StudyCompletedError()
        return study_id

    def create(self, validated_data):
        """
        Create and return a new `Submission` instance, given the validated data.
        """
        return Submission.objects.create(**validated_data)

from rest_framework import generics, status
from rest_framework.response import Response
from prolific.exceptions import InvalidActionError, StudyCompletedError
from prolific.models import Study, Submission
from prolific.serializers import StudySerializer, SubmissionSerializer


class StudyView(generics.ListCreateAPIView):
    serializer_class = StudySerializer
    queryset = Study.objects.all()

    def get(self, request, *args, **kwargs):
        surveys = Study.objects.all()
        serializer = StudySerializer(surveys, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StudySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudySubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get(self, request, *args, **kwargs):
        study = Study.objects.get(id=kwargs["study_id"])
        submissions = Submission.objects.filter(study=study)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)


class SubmissionView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get(self, request, *args, **kwargs):
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except StudyCompletedError:
                return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmissionUpdateView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        sub = Submission.objects.get(id=kwargs["submission_id"])
        if request.data["action"] == "complete":
            sub.complete()
            serializer = SubmissionSerializer(sub)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise InvalidActionError()

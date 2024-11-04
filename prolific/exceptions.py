from rest_framework import exceptions, status


class StudyCompletedError(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "This study has already been completed."


class InvalidActionError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "The requested action is not valid."

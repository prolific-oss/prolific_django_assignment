

from django.urls import path

from prolific import views

urlpatterns = [
    path(
        'studies/',
        views.StudyView.as_view(),
        name="studies"
    ),
    path(
        'studies/<study_id>/submissions/',
        views.StudySubmissionsView.as_view(),
        name="study_submission_list"
    ),
    path(
        'submissions/',
        views.SubmissionView.as_view(),
        name="submissions"
    ),
    path(
        'submissions/<submission_id>/',
        views.SubmissionUpdateView.as_view(),
        name="submission_update"
    ),
]

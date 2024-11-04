from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from prolific import constants
from prolific.models import Study, Submission


class TestStudyView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("studies")

    def test_list_all_studies(self):
        study = Study.objects.create(name="test study list", total_places=1, user_id=1)
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.data[0],
            {
                "id": 1,
                "name": "test study list",
                "total_places": 1,
                "user_id": 1,
                "status": "ACTIVE"
            }
        )

    def test_create_study(self):
        data = {"name": "test create study", "total_places": 1, "user_id": 1}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Study.objects.count(), 1)

        study = Study.objects.get()

        self.assertEqual(study.id, 1)
        self.assertEqual(study.name, "test create study")
        self.assertEqual(study.total_places, 1)
        self.assertEqual(study.user_id, 1)
        self.assertEqual(study.status, "ACTIVE")


class TestStudySubmissionsView(APITestCase):
    def test_list_all_study_submissions(self):
        study = Study.objects.create(name="test list all submissions", total_places=1, user_id=1)
        url = reverse("study_submission_list", kwargs={"study_id": study.id})
        sub = Submission.objects.create(study=study, user_id=2)
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["study_id"], 1)
        self.assertEqual(response.data[0]["user_id"], 2)
        self.assertIsNotNone(response.data[0]["started_at"])
        self.assertIsNone(response.data[0]["completed_at"])


class TestSubmissionView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("submissions")

    def test_list_all_submissions(self):
        study = Study.objects.create(name="test list all submissions", total_places=1, user_id=1)
        sub = Submission.objects.create(study=study, user_id=2)
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["study_id"], 1)
        self.assertEqual(response.data[0]["user_id"], 2)
        self.assertIsNotNone(response.data[0]["started_at"])
        self.assertIsNone(response.data[0]["completed_at"])

    def test_create_submission(self):
        study = Study.objects.create(name="test create submission", total_places=1, user_id=1)
        data = {"study_id": 1, "user_id": 2}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Submission.objects.count(), 1)

        sub = Submission.objects.get()

        self.assertEqual(sub.id, 1)
        self.assertEqual(sub.study_id, 1)
        self.assertEqual(sub.user_id, 2)
        self.assertIsNotNone(sub.started_at)
        self.assertIsNone(sub.completed_at)


class TestSubmissionUpdateView(APITestCase):
    def test_complete_submission(self):
        study = Study.objects.create(name="test complete submission", total_places=1, user_id=1)
        sub = Submission.objects.create(study=study, user_id=2)
        url = reverse("submission_update", kwargs={"submission_id": sub.id})
        data = {"action": "complete"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sub.status, constants.STATUS_COMPLETED)

from datetime import datetime
from django.db import models
from prolific import constants


class Study(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    total_places = models.IntegerField()
    user_id = models.IntegerField()

    @property
    def status (self):
        if Submission.objects.filter(study=self, status=constants.STATUS_COMPLETED).count() == self.total_places:
            return constants.STATUS_COMPLETED
        return constants.STATUS_ACTIVE


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    status = models.CharField(choices=constants.STATUSES, default=constants.STATUS_ACTIVE, max_length=20)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, default=None)

    def complete(self):
        self.status = constants.STATUS_COMPLETED
        self.completed_at = datetime.now()
        self.save()

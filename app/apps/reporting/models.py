from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TaskReport(models.Model):
    WORKFLOW_STATE_QUEUED = 0
    WORKFLOW_STATE_STARTED = 1
    WORKFLOW_STATE_ERROR = 2
    WORKFLOW_STATE_DONE = 3
    WORKFLOW_STATE_CHOICES = (
        (WORKFLOW_STATE_QUEUED, _("Queued")),
        (WORKFLOW_STATE_STARTED, _("Running")),
        (WORKFLOW_STATE_ERROR, _("Crashed")),
        (WORKFLOW_STATE_DONE, _("Finished"))
    )

    workflow_state = models.PositiveSmallIntegerField(
        default=WORKFLOW_STATE_QUEUED,
        choices=WORKFLOW_STATE_CHOICES
    )
    label = models.CharField(max_length=256)
    messages = models.TextField(blank=True)

    queued_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    done_at = models.DateTimeField(null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # celery task id
    task_id = models.CharField(max_length=64, blank=True, null=True)

    # shared_task method name
    method = models.CharField(max_length=512, blank=True, null=True)

    cpu_cost = models.FloatField(blank=True, null=True)
    gpu_cost = models.FloatField(blank=True, null=True)

    def append(self, text):
        self.messages += text + '\n'

    @property
    def uri(self):
        return reverse('report-detail', kwargs={'pk': self.pk})

    def start(self, task_id, method):
        self.task_id = task_id
        self.method = method
        self.workflow_state = self.WORKFLOW_STATE_STARTED
        self.started_at = datetime.now(timezone.utc)
        self.save()

    def error(self, message):
        # unrecoverable error
        self.workflow_state = self.WORKFLOW_STATE_ERROR
        self.done_at = datetime.now(timezone.utc)
        self.append(message)
        self.save()

    def end(self, extra_links=None):
        self.workflow_state = self.WORKFLOW_STATE_DONE
        self.done_at = datetime.now(timezone.utc)
        self.save()

    def calc_cpu_cost(self, nb_cores):
        task_duration = (self.done_at - self.started_at).total_seconds()
        self.cpu_cost = (task_duration * nb_cores * settings.CPU_COST_FACTOR) / 60
        self.save()

    def calc_gpu_cost(self):
        task_duration = (self.done_at - self.started_at).total_seconds()
        self.gpu_cost = (task_duration * settings.GPU_COST) / 60
        self.save()

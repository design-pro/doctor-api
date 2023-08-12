from django.db import models


class CommonModel(models.Model):
    title = models.CharField(max_length=1024)
    update_at = models.DateTimeField(
        auto_now=True, verbose_name="زمان بروز رسانی")
    created_at = models.DateTimeField(
        verbose_name="زمان ثبت", auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(
        verbose_name="زمان ثبت", null=True, blank=True)

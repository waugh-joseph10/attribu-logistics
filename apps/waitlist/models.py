from django.db import models


class WaitlistEntry(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50, default="landing")

    class Meta:
        verbose_name_plural = "waitlist entries"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

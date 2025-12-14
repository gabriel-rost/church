from django.db import models

class Content(models.Model):
    title = models.CharField(max_length=256, blank=True)
    text = models.TextField(blank=False)

    attachments = models.ManyToManyField(
        "church_app.Archive",
        blank=True,
        related_name="contents"
    )

    def __str__(self):
        return self.text[:50]
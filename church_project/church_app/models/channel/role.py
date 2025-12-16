from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, max_length=300)

    def __str__(self):
        return self.name
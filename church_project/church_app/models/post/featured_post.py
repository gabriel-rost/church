from django.db import models

class FeaturedPost(models.Model):
    post = models.OneToOneField("Post", on_delete=models.CASCADE, related_name="featured_post")
    featured_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Featured Post: {self.post} (Featured on {self.featured_date})"
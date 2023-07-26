from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    url_link = models.URLField(max_length=200, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    png_with_qr = models.FileField(null=True, blank=True)
    shortened_link = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.url_link

    class Meta:
        ordering = ['-date_added']




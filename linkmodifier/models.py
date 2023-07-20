from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    url_link = models.URLField(max_length=200, null=False, blank=False,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.url_link

    class Meta:
        ordering = ['-date_added']

class QrCode(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True)
    png_with_qr = models.FileField(null=True, blank=True)
    link = models.ForeignKey(Link,
                             to_field='url_link',
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False,
                             )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link
    class Meta:
        ordering = ['-date_added']
class ShortLink(models.Model):
    title = models.CharField(max_length=20, null=True, blank=True, unique=True)
    link = models.ForeignKey(Link,
                             to_field='url_link',
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False,
                             )
    shortened_link = models.URLField(max_length=200, null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.shortened_link
    class Meta:
        ordering = ['-date_added']
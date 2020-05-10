from django.db import models

# Create your models here.
class faceEncodings(models.Model):
    user_name = models.CharField(max_length=200)
    encodings = models.TextField()

    def __str__(self):
        return self.user_name
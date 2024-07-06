from django.db import models

# This model is not used in the current implementation but kept for reference
class Details(models.Model):
    qrcode = models.ImageField(upload_to="images/")
    _id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    caste = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self._id} - {self.name}"
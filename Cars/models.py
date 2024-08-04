from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    fueltype = models.CharField(max_length=50)
    drive = models.CharField(max_length=50)
    displ = models.FloatField()
    city08 = models.FloatField()
    highway08 = models.FloatField()
    co2 = models.FloatField()
    fuelcost08 = models.FloatField()
    trany = models.CharField(max_length=50)
    vclass = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

from django.db import models

class EnergyData(models.Model):
    date = models.IntegerField()
    region = models.CharField(max_length=100)
    consumption_twh = models.FloatField()

    def __str__(self):
        return f"Energy data for {self.region} on {self.date}"

from django.db import models

class Product(models.Model):
    ean13 = models.CharField(max_length=255)
    pasutijuma_kods = models.CharField(max_length=255, unique=True, null=True)
    apraksts = models.TextField(blank=True)
    attels = models.URLField(blank=True)
    cena = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.ean13  # Changed from self.name to self.ean13
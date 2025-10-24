from django.db import models

class Author(models.Model):
    first_name = models.CharField(verbose_name="Vardas", max_length=30)
    last_name = models.CharField(verbose_name="Pavardė", max_length=30)

    def __str__(self):
        return f"Autorius {self.first_name} {self.last_name}"
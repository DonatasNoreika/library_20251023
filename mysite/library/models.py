from django.db import models

class Author(models.Model):
    first_name = models.CharField(verbose_name="Vardas", max_length=30)
    last_name = models.CharField(verbose_name="Pavardė", max_length=30)

    def __str__(self):
        return f"Autorius {self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas")
    summary = models.TextField(verbose_name="Aprašymas")
    isbn = models.CharField(verbose_name="ISBN")
    author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ManyToManyField(to="Genre", verbose_name="Žanras")

    def __str__(self):
        return self.title
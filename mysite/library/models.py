from django.db import models
import uuid

class Author(models.Model):
    first_name = models.CharField(verbose_name="Vardas", max_length=30)
    last_name = models.CharField(verbose_name="Pavardė", max_length=30)

    def __str__(self):
        return f"Autorius {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"

class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas")
    summary = models.TextField(verbose_name="Aprašymas")
    isbn = models.CharField(verbose_name="ISBN")
    author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ManyToManyField(to="Genre", verbose_name="Žanras")

    def display_genre(self):
        genres = self.genre.all()
        result = ""
        for genre in genres:
            result += genre.name + ", "
        return result

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural = "Knygos"

class BookInstance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    book = models.ForeignKey(to="Book", verbose_name="Knyga", on_delete=models.CASCADE)
    due_back = models.DateField(verbose_name="Grąžinimo data", null=True, blank=True)

    LOAN_STATUS = (
        ('d', "Administered"),
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(verbose_name="Būsena", max_length=1, choices=LOAN_STATUS, default="d", blank=True)

    def __str__(self):
        return f"{self.book.title} ({self.uuid})"

    class Meta:
        verbose_name = "Kopija"
        verbose_name_plural = "Kopijos"

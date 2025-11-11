from django.db import models
import uuid
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    first_name = models.CharField(verbose_name=_("First Name"), max_length=30)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=30)
    description = HTMLField(verbose_name=_("Description"), null=True, blank=True)

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    display_books.short_description = _("Books")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

class Genre(models.Model):
    name = models.CharField(verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

class Book(models.Model):
    title = models.CharField(verbose_name=_("Title"))
    summary = models.TextField(verbose_name=_("Summary"))
    isbn = models.CharField(verbose_name="ISBN")

    author = models.ForeignKey(to="Author",
                               verbose_name=_("Author"),
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name="books")

    genre = models.ManyToManyField(to="Genre", verbose_name=_("Genre"))
    cover = models.ImageField(verbose_name=_("Cover"), upload_to="covers", null=True, blank=True)

    def display_genre(self):
        genres = self.genre.all()
        result = ""
        for genre in genres:
            result += genre.name + ", "
        return result

    display_genre.short_description = _("Genres")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

class BookInstance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    book = models.ForeignKey(to="Book",
                             verbose_name=_("Book"),
                             on_delete=models.CASCADE,
                             related_name="instances")
    due_back = models.DateField(verbose_name=_("Due Back"), null=True, blank=True)
    reader = models.ForeignKey(to="library.CustomUser", verbose_name=_("Reader"), on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('d', _("Administered")),
        ('t', _('Taken')),
        ('a', _('Available')),
        ('r', _('Reserved')),
    )

    status = models.CharField(verbose_name=_("Status"), max_length=1, choices=LOAN_STATUS, default="d", blank=True)

    def is_overdue(self):
        return self.due_back and timezone.now().date() > self.due_back

    is_overdue.short_description = _("Is overdue")

    def __str__(self):
        return f"{self.book.title} ({self.uuid})"

    class Meta:
        verbose_name = _("Instance")
        verbose_name_plural = _("Instances")


class BookReview(models.Model):
    book = models.ForeignKey(to="Book",
                             verbose_name=_("Book"),
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name="reviews")
    reviewer = models.ForeignKey(to="library.CustomUser", verbose_name=_("Reviewer"), on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True)
    content = models.TextField(verbose_name=_("Content"))

    class Meta:
        verbose_name = _("Book Review")
        verbose_name_plural = _("Book Reviews")
        ordering = ['-pk']


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profile_pics", verbose_name=_("Photo"), null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)
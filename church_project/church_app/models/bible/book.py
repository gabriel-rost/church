from django.db import models
from django.utils.text import slugify

class Book(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True) # Para URLs amigáveis
    order = models.PositiveIntegerField(unique=True) # Garante que não haja ordem repetida

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.book.name} {self.number}"

    class Meta:
        # Impede a criação de capítulos duplicados para o mesmo livro
        unique_together = ('book', 'number')
        ordering = ['number']

class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='verses')
    number = models.PositiveIntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.number}"

    class Meta:
        # Impede versículos duplicados no mesmo capítulo
        unique_together = ('chapter', 'number')
        ordering = ['number']
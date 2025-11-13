from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not manually set
        if not self.slug or self.title_changed():
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def title_changed(self):
        """Helper method to check if title has changed (for updates)."""
        if not self.pk:
            return True  # It's new
        old_title = Category.objects.filter(pk=self.pk).values_list('title', flat=True).first()
        return old_title != self.title
    
    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
from django.db import models


class Country(models.Model):
    """
    Abstract class for reduce size of lines .. ;)
    """
    title = models.TextField(max_length=100)
    is_live = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        self.title = self.title.lower()

    class Meta:
        ordering = ('title',)


class State(models.Model):
    """
    Abstract class for reduce size of lines .. ;)
    """
    title = models.TextField(max_length=100)
    country = models.ForeignKey('country_state.Country')
    is_live = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        self.title = self.title.lower()

    class Meta:
        ordering = ('title',)

# Create your models here.

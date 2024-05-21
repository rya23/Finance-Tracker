from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    cost = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateField("Date")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category}: {self.cost}"


class Income(models.Model):
    cost = models.IntegerField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField("Date")

    def __str__(self):
        return f"{self.source}: {self.cost}"

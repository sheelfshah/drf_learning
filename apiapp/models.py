# models defined here
# no model has a separate primary key field,
# as it is available already as modelname.pk

from django.db import models


class Country(models.Model):

    name = models.CharField(max_length=100, unique=True)  # read_only
    description = models.TextField(max_length=1000)  # to set textbox size
    population = models.IntegerField()
    GDP = models.FloatField()

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class State(models.Model):

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=100, unique=True)  # read_only
    description = models.TextField(max_length=1000)  # to set textbox size
    population = models.IntegerField()
    GDP = models.FloatField()

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"

    def __str__(self):
        return self.name


class CityTown(models.Model):
    """
        Instead of creating separate city and town models,
        created one model with is_city field.
    """

    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='citytowns')
    # no need to add country, since it can be retrieved from state

    name = models.CharField(max_length=100, unique=True)  # read_only
    description = models.TextField(max_length=1000)  # to set textbox size
    population = models.IntegerField()
    GDP = models.FloatField()
    pincode = models.CharField(max_length=20)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"

    def __str__(self):
        return self.name


class Person(models.Model):

    name = models.CharField(max_length=200)
    citytown = models.ForeignKey(
        CityTown, on_delete=models.CASCADE, related_name='persons')

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return self.name

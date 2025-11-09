from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=255)
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=255, null=True, blank=True)
    summer = models.CharField(max_length=255, null=True, blank=True)
    autumn = models.CharField(max_length=255, null=True, blank=True)
    spring = models.CharField(max_length=255, null=True, blank=True)


class Pereval(models.Model):
    STATUS_CHOICES = (
        ("new", "новый"),
        ("pending", "в работе"),
        ("accepted", "принят"),
        ("rejected", "отклонен")
    )
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=255, null=True, blank=True)
    add_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")


class Images(models.Model):
    data = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
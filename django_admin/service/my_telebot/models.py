from django.db import models


class Cities(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_spots(self):
        return ",  ".join([child.name for child in self.spots.all()])


# Create your models here.
class User(models.Model):
    city = models.ForeignKey(Cities, related_name='user', on_delete=models.CASCADE, default=None)
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    language_code = models.CharField(max_length=8, null=True, blank=True, help_text="Telegram client's lang")

    is_blocked_bot = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    get_remainder = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'


class Spots(models.Model):
    city = models.ForeignKey(Cities, related_name='spots', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, null=False, blank=False, unique=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    url_map = models.URLField(default='')
    url_forecast = models.URLField(default='')

    lat = models.DecimalField(max_digits=21, decimal_places=18)
    lon = models.DecimalField(max_digits=21, decimal_places=18)

    wind_degree_l = models.FloatField()
    wind_degree_r = models.FloatField()
    wind_min = models.FloatField()
    wind_max = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

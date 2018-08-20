from django.db import models


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=32)
    version = models.CharField(max_length=16,
                               blank=True, null=True)
    release = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class LeaderBoard(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE,
                                 blank=True, null=True)
    organizer = models.CharField(max_length=256)
    score = models.FloatField()
    time = models.CharField(max_length=16)
    country = models.CharField(max_length=128)

    @property
    def get_language(self):
        return self.language.name

    def __str__(self):
        return self.name

# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Termin(models.Model):
    datum = models.DateField()
    beginn = models.TimeField()
    ende = models.TimeField()

    class Meta:
        db_table = 'termin'

    def clean(self):
        if self.beginn > self.ende:
            raise ValidationError(u'Ende darf nicht vor Beginn stattfinden!')

    def __unicode__(self):
        return (unicode(self.datum) + u' ' + unicode(self.beginn) + u' - ' +
                unicode(self.ende))


class Fach(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'fach'

    def __unicode__(self):
        return self.name


class Kursgruppe(models.Model):
    thema = models.CharField(max_length=200)
    max_tn = models.IntegerField()
    fach = models.ForeignKey(Fach)
    termine = models.ManyToManyField(Termin, db_table='findet_statt_an')

    class Meta:
        db_table = 'kursgruppe'

    def __unicode__(self):
        return self.thema


class Student(models.Model):
    user = models.OneToOneField(User)
    matrikelnummer = models.IntegerField(unique=True)
    belegen = models.ManyToManyField(Kursgruppe,
                                     db_table='student_belegt_kurs',
                                     related_name='belegende_studenten')
    haben_belegt = models.ManyToManyField(Kursgruppe,
                                          db_table='student_hat_kurs_belegt',
                                          related_name='studenten_haben_belegt')

    class Meta:
        db_table = 'student'

    def __unicode__(self):
        return (self.user.first_name + u' ' + self.user.last_name + u' ' +
                unicode(self.matrikelnummer))

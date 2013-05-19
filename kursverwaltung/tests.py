# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from models import Student, Termin

import datetime

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError


def create_student(username, first_name, last_name, email, matrikelnr,
                   pw=None):
    """
    Erzeugt einen neuen Studenten.
    """
    s = Student.objects.create(
        user=User.objects.create_user(username, email, pw,
                                      first_name=first_name,
                                      last_name=last_name),
        matrikelnummer=matrikelnr
    )
    return s


def create_Testingtons():
    create_student('alice', 'Alice', 'Testington', 'alice@example.org',
                   6660001, '')
    create_student('bob', 'Bob', 'Testington', 'bob@example.org',
                   6660002, '')
    create_student('charles', 'Charles', 'Testington',
                   'charles@example.org', 6660003, '')
    create_student('david', 'David', 'Testington', 'david@example.org',
                   6660004, '')
    create_student('eve', 'Eve', 'Testington', 'eve@example.org',
                   6660005, '')


class StudentenTests(TestCase):
    def setUp(self):
        self.students = dict()
        self.students['alice'] = create_student(
            'alice', 'Alice', 'Testington', 'alice@example.org', 6660001, ''
        )
        self.students['bob'] = create_student(
            'bob', 'Bob', 'Testington', 'bob@example.org', 6660002, ''
        )
        self.students['charles'] = create_student(
            'charles', 'Charles', 'Testington', 'charles@example.org', 6660003,
            ''
        )
        self.students['david'] = create_student(
            'david', 'David', 'Testington', 'david@example.org', 6660004, ''
        )
        self.students['eve'] = create_student(
            'eve', 'Eve', 'Testington', 'eve@example.org', 6660005, ''
        )

    def test_retrieve_student_via_matrikelnummer(self):
        """
        Holt 'alice' per Matrikelnummer aus der Datenbank.
        """
        self.assertEqual(Student.objects.get(matrikelnummer=6660001),
                         self.students['alice'])

    def test_retrieve_student_via_username(self):
        """
        Holt 'bob' per Benutzername aus der Datenbank.
        """
        self.assertEqual(
            Student.objects.get(user__username='bob'),
            self.students['bob']
        )

    def test_retrieve_student_via_full_name_and_matrikelnummer(self):
        self.assertEqual(
            Student.objects.get(
                user__first_name='Charles',
                user__last_name='Testington',
                matrikelnummer=6660003),
            self.students['charles']
        )

    def test_retrieve_student_by_email(self):
        self.assertEqual(
            Student.objects.get(
                user__email='david@example.org'),
            self.students['david']
        )

    def test_retrieve_Testingtons(self):
        """
        In der Datenbank müssten sich 5 Testingtons befinden.
        """
        self.assertEqual(
            len(Student.objects.filter(
                user__last_name='Testington')),
            5
        )

    def test_remove_student_via_username(self):
        """
        Entfernt 'eve' und überprüft, ob sie noch vorhanden ist
        """
        Student.objects.get(user__username='eve').delete()

        self.assertRaises(
            ObjectDoesNotExist,
            Student.objects.get,
            user__username='eve'
        )

    def test_remove_student_via_matrikelnummer(self):
        """
        Entfernt 'david' mittels Matrikelnummer.
        """
        Student.objects.get(matrikelnummer=6660004).delete()

        self.assertRaises(
            ObjectDoesNotExist,
            Student.objects.get,
            matrikelnummer=6660004
        )

    def test_create_already_existing_student(self):
        """
        Erzeugt 'eve', die aber schon existiert.
        """

        self.assertRaises(
            IntegrityError,
            create_student,
            'eve', 'Eve', 'Testington', 'eve@example.org', 6660005, ''
        )

    def test_change_matrikelnummer(self):
        """
        Ändert die Matrikelnummer von 'alice'.
        """
        Student.objects.filter(user__username='alice').update(
            matrikelnummer=6660006
        )

        self.assertEqual(
            Student.objects.get(user__username='alice').matrikelnummer,
            6660006
        )


class TerminTests(TestCase):
    def setUp(self):
        Termin.objects.create(
            datum=datetime.date(2013, 9, 30),
            beginn=datetime.time(9, 0),
            ende=datetime.time(18, 0)
        )
        Termin.objects.create(
            datum=datetime.date(2013, 1, 13),
            beginn=datetime.time(11, 15),
            ende=datetime.time(12, 45)
        )
        Termin.objects.create(
            datum=datetime.date(2013, 5, 13),
            beginn=datetime.time(11, 15),
            ende=datetime.time(12, 45)
        )
        Termin.objects.create(
            datum=datetime.date(2013, 11, 13),
            beginn=datetime.time(11, 15),
            ende=datetime.time(12, 45)
        )

    def test_create_Termin(self):
        """
        Testet, ob ein erstellter Termin auch wirklich vorhanden ist.
        """
        Termin.objects.create(
            datum=datetime.date(2013, 2, 13),
            beginn=datetime.time(11, 15),
            ende=datetime.time(12, 45)
        )

        t = Termin.objects.get(datum='2013-2-13', beginn='11:15', ende='12:45')

        self.assertEqual(t.datum, datetime.date(2013, 2, 13))
        self.assertEqual(t.beginn, datetime.time(11, 15))
        self.assertEqual(t.ende, datetime.time(12, 45))

    def test_create_already_existing_termin(self):
        """
        Ein schon existierender Termin darf nicht nochmal vergeben werden.
        """
        self.assertRaises(
            IntegrityError,
            Termin.objects.create,
            datum=datetime.date(2013, 9, 30),
            beginn=datetime.time(9, 0),
            ende=datetime.time(18, 0)
        )

    def test_semester_function(self):
        """
        Testet, ob semester() auch das richtige Semester liefert.
        """
        self.assertEqual(
            Termin.objects.get(
                datum='2013-1-13',
                beginn='11:15',
                ende='12:45').semester,
            'WS 2012 2013'
        )
        self.assertEqual(
            Termin.objects.get(
                datum='2013-5-13',
                beginn='11:15',
                ende='12:45').semester,
            'SS 2013'
        )
        self.assertEqual(
            Termin.objects.get(
                datum='2013-11-13',
                beginn='11:15',
                ende='12:45').semester,
            'WS 2013 2014'
        )
        self.assertNotEqual(
            Termin.objects.get(
                datum='2013-11-13',
                beginn='11:15',
                ende='12:45').semester,
            'SS 2013'
        )

    def test_incorrect_termin(self):
        """
        Testet, ob falsche Termine möglich sind.
        """
        self.assertRaises(
            ValidationError,
            Termin.objects.create,
            datum=datetime.date(2013, 1, 1),
            beginn=datetime.time(13, 0),
            ende=datetime.time(11, 0)
        )

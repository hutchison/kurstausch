# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from kursverwaltung.models import Kursgruppe, Student, Fach, Termin

from django.utils.translation import ugettext_lazy as _


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False


class StudentsUserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions'),
                            'classes': ['collapse']}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined'),
                                'classes': ['collapse']}),
    )
    inlines = [StudentInline]


class BelegendeStudentenInline(admin.StackedInline):
    model = Student.belegen.through
    extra = 1


class KursgruppeInline(admin.StackedInline):
    model = Kursgruppe
    can_delete = False
    extra = 1


class FachAdmin(admin.ModelAdmin):
    inlines = [KursgruppeInline]


class KursgruppenAdmin(admin.ModelAdmin):
    list_display = ('thema', 'fach', 'max_tn', 'num_tn', 'is_full')
    inlines = [BelegendeStudentenInline]
    search_fields = ['thema', 'fach__name']


class StattfindendeKursgruppenInline(admin.StackedInline):
    model = Kursgruppe.termine.through
    extra = 1


class TerminAdmin(admin.ModelAdmin):
    list_display = ('datum', 'beginn', 'ende', 'semester')
    inlines = [StattfindendeKursgruppenInline]


admin.site.unregister(User)
admin.site.register(User, StudentsUserAdmin)

admin.site.register(Kursgruppe, KursgruppenAdmin)
admin.site.register(Fach, FachAdmin)
admin.site.register(Termin, TerminAdmin)

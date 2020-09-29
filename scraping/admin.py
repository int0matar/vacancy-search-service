from django.contrib import admin

from .models import Location, Specialty, Vacancy, Url, Error


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'slug')
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'slug')
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    search_fields = ('id', 'location', 'specialty', 'title', 'company',
                     'description', 'date',)
    list_display = ('id', 'location', 'specialty', 'title', 'company', 'date',)
    list_filter = ('specialty', 'company', 'date')
    list_display_links = ('title',)


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    search_fields = ('id', 'location', 'specialty', 'url_json')
    list_display = ('id', 'location', 'specialty', 'url_json')


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    search_fields = ('id', 'error_json', 'date')
    list_display = ('id', 'date', 'error_json')
    list_filter = ('date',)
    list_display_links = ('error_json',)

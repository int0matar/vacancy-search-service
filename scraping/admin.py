from django.contrib import admin

from .models import City, Language, Vacancy, UrlAddress, ErrorLog


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'slug')
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name', 'slug')
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title', 'company', 'city', 'language',
                     'description', 'timestamp')
    list_filter = ('language', 'company', 'timestamp')
    list_display = ('id', 'title', 'company', 'city', 'language', 'timestamp')
    list_display_links = ('title',)


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    search_fields = ('id', 'error_data', 'timestamp')
    list_filter = ('timestamp',)
    list_display = ('id', 'timestamp', 'error_data')


@admin.register(UrlAddress)
class UrlAddressAdmin(admin.ModelAdmin):
    search_fields = ('id', 'city', 'language', 'url_data')
    list_display = ('id', 'city', 'language', 'url_data')

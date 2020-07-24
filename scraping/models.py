from django.db import models
import jsonfield

from scraping.utils import icao_transliter


def default_url():
    return {'work_ua': '', 'rabota_ua': '', 'dou_ua': '', 'djinni_co': ''}


class City(models.Model):
    name = models.CharField(verbose_name='Название населенного пункта',
                            max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = icao_transliter(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(verbose_name='Язык программирования',
                            max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = icao_transliter(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(verbose_name='Заголовок вакансии', max_length=250)
    company = models.CharField(verbose_name='Компания', max_length=250)
    description = models.TextField(verbose_name='Описание вакансии')
    timestamp = models.DateField(verbose_name='Дата', auto_now_add=True)
    city = models.ForeignKey('City', verbose_name='Город',
                             on_delete=models.CASCADE)
    language = models.ForeignKey('Language',
                                 verbose_name='Язык программирования',
                                 on_delete=models.CASCADE)
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title


class UrlAddress(models.Model):
    city = models.ForeignKey('City', verbose_name='Город',
                             on_delete=models.CASCADE)
    language = models.ForeignKey('Language',
                                 verbose_name='Языки программирования',
                                 on_delete=models.CASCADE)
    url_data = jsonfield.JSONField(verbose_name='Адрес', default=default_url)

    class Meta:
        unique_together = ('city', 'language')
        verbose_name = 'URL-Адрес'
        verbose_name_plural = 'URL-Адреса'

    def __str__(self):
        return self.url_data


class ErrorLog(models.Model):
    error_data = jsonfield.JSONField()
    timestamp = models.DateField(verbose_name='Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'

    def __str__(self):
        return self.timestamp

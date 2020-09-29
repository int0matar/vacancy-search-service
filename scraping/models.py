from django.db import models
import jsonfield

from scraping.utils import transliteration, default_url


class Location(models.Model):
    name = models.CharField(verbose_name='Населенный пункт',
                            max_length=50,
                            unique=True)
    slug = models.SlugField(verbose_name='Линк',
                            max_length=50,
                            unique=True,
                            blank=True)

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliteration(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(verbose_name='Специальность',
                            max_length=50,
                            unique=True)
    slug = models.SlugField(verbose_name='Линк',
                            max_length=50,
                            unique=True,
                            blank=True)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliteration(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    location = models.ForeignKey('scraping.Location',
                                 verbose_name='Город',
                                 on_delete=models.CASCADE,
                                 null=True)
    specialty = models.ForeignKey('scraping.Specialty',
                                  verbose_name='Специальность',
                                  on_delete=models.CASCADE,
                                  null=True)
    title = models.CharField(verbose_name='Заголовок вакансии',
                             max_length=250,
                             blank=True)
    company = models.CharField(verbose_name='Компания',
                               max_length=250,
                               blank=True)
    description = models.TextField(verbose_name='Описание вакансии',
                                   max_length=5000,
                                   blank=True)
    url = models.URLField(unique=True)
    date = models.DateField(verbose_name='Дата', auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title


class Url(models.Model):
    location = models.ForeignKey('scraping.Location',
                                 verbose_name='Город',
                                 on_delete=models.CASCADE,
                                 null=True)
    specialty = models.ForeignKey('scraping.Specialty',
                                  verbose_name='Специальность',
                                  on_delete=models.CASCADE,
                                  null=True)
    url_json = jsonfield.JSONField(verbose_name='Адрес', default=default_url)

    class Meta:
        unique_together = ('location', 'specialty')
        verbose_name = 'URL-Адрес'
        verbose_name_plural = 'URL-Адреса'

    def __str__(self):
        return str(self.url_json)


class Error(models.Model):
    error_json = jsonfield.JSONField(verbose_name='Данные ошибок')
    date = models.DateField(verbose_name='Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'

    def __str__(self):
        return str(self.date)

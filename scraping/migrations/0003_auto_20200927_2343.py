# Generated by Django 3.1.1 on 2020-09-27 17:43

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200927_2343'),
        ('scraping', '0002_auto_20200907_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Населенный пункт')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Линк')),
            ],
            options={
                'verbose_name': 'Населенный пункт',
                'verbose_name_plural': 'Населенные пункты',
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Специальность')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Линк')),
            ],
            options={
                'verbose_name': 'Специальность',
                'verbose_name_plural': 'Специальности',
            },
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-date'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
        migrations.RenameField(
            model_name='error',
            old_name='timestamp',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='url_in_json',
            new_name='url_json',
        ),
        migrations.RenameField(
            model_name='vacancy',
            old_name='timestamp',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='vacancy',
            old_name='url_field',
            new_name='url',
        ),
        migrations.RemoveField(
            model_name='error',
            name='error',
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='city',
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='language',
        ),
        migrations.AddField(
            model_name='error',
            name='error_json',
            field=jsonfield.fields.JSONField(default=dict, verbose_name='Данные ошибок'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.CharField(blank=True, max_length=250, verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.TextField(blank=True, max_length=5000, verbose_name='Описание вакансии'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='title',
            field=models.CharField(blank=True, max_length=250, verbose_name='Заголовок вакансии'),
        ),
        migrations.AddField(
            model_name='url',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.location', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='url',
            name='specialty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.specialty', verbose_name='Специальность'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.location', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='specialty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.specialty', verbose_name='Специальность'),
        ),
        migrations.AlterUniqueTogether(
            name='url',
            unique_together={('location', 'specialty')},
        ),
        migrations.RemoveField(
            model_name='url',
            name='city',
        ),
        migrations.RemoveField(
            model_name='url',
            name='language',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]

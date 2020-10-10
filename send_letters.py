import os
import sys
import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
django.setup()

from scraping.models import Vacancy, Url, Error
from scraping_service.settings import EMAIL_HOST_ADMIN, EMAIL_HOST_USER


User = get_user_model()

current_day = datetime.date.today()

administrator_email = EMAIL_HOST_ADMIN

from_email = EMAIL_HOST_USER


# Sends an email if there are vacancies on the current date
subscribed_users = User.objects.filter(is_subscriber=True) \
                               .values('location', 'specialty', 'email')

user_with_pair_id_and_email = {}

for user in subscribed_users:
    user_with_pair_id_and_email.setdefault((user['location'],
                                            user['specialty']), [])
    user_with_pair_id_and_email[(user['location'],
                                 user['specialty'])].append(user['email'])

if user_with_pair_id_and_email:
    where_id = {'location_id__in': [], 'specialty_id__in': []}

    for pair_id in user_with_pair_id_and_email.keys():
        where_id['location_id__in'].append(pair_id[0])
        where_id['specialty_id__in'].append(pair_id[1])

    currently_vacancies = Vacancy.objects.filter(**where_id,
                                                 auto_date=current_day) \
                                         .values()[:10]
    vacancies = {}

    for vacancy in currently_vacancies:
        vacancies.setdefault((vacancy['location_id'],
                              vacancy['specialty_id']), [])
        vacancies[(vacancy['location_id'],
                   vacancy['specialty_id'])].append(vacancy)

    for pair_id, emails in user_with_pair_id_and_email.items():
        rows = vacancies.get(pair_id, [])
        content = ''

        for row in rows:
            content += f'<h5><a href="{row["url"]}">{row["title"]}</a></h5>'
            content += f'<p>{row["description"]}</p>'
            content += f'<p>{row["company"]}</p><br<hr>'

        empty_email = '<h3>По Вашим предпочтениям новых вакансий нет.</h3>'
        html_content = content if content else empty_email

        for each_recipient in emails:
            subject = f'CatchWork. Вакансии за {current_day}'
            text_content = 'Вакансии'
            to = each_recipient
            message = EmailMultiAlternatives(
                subject,
                text_content,
                from_email,
                [to],
            )
            message.attach_alternative(html_content, "text/html")
            message.send()


# Sends an email if there is an error
currently_errors = Error.objects.filter(auto_date=current_day)

if currently_errors.exists():
    take_the_first = currently_errors.first()
    error = take_the_first.error
    html_content = ''

    for error in error:
        subject = f'CatchWork. Ошибки за {current_day}'
        text_content = 'Ошибка'
        html_content += f'<p><a href="{error["url"]}">{error["title"]}</a></p>'
        to = administrator_email
        message = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [to],
        )
        message.attach_alternative(html_content, "text/html")
        message.send()


# Sends an email if there is an empty URL
url_values = Url.objects.all().values('location', 'specialty')

urls = {(value_id['location'],
         value_id['specialty']): True for value_id in url_values}

html_content = ''

for pair_id in urls.keys():
    if pair_id not in urls:
        subject = 'Отсутствует URL'
        text_content = 'Ошибка'
        html_content += f'<p>Город: {pair_id[0]}, специальность: {pair_id[1]},'\
                         ' отсутствует URL</p><br>'
        to = administrator_email
        message = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [to],
        )
        message.attach_alternative(html_content, "text/html")
        message.send()

import os
import sys
import django
import asyncio
from django.db import DatabaseError
from django.contrib.auth import get_user_model

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
django.setup()

from scraping.models import Vacancy, Url, Error
from scraping.parsers import *


User = get_user_model()

data_for_recording_vacancies = []
data_for_recording_errors = []

parsers = ((work_ua, 'work_ua'),
           (rabota_ua, 'rabota_ua'),
           (dou_ua, 'dou_ua'),
           (djinni_co, 'djinni_co'))

def get_unique_pair():
    """
    Returns unique id pairs of tuple by city and language
    """
    subscribed_users = User.objects.filter(is_subscriber=True).values()
    unique_pair_of_user = set(
        (value_id['location_fk_id'], value_id['specialty_fk_id'])
        for value_id in subscribed_users
    )
    return unique_pair_of_user


def get_pair_id_with_url(pair_id):
    """
    Returns list with dictionary by unique tuple of get_unique_pair method
    and field Url.url_json_field
    """
    url_values = Url.objects.all().values()
    pair_id_with_urls = {
        (value_id['location_fk_id'], value_id['specialty_fk_id']):
        value_id['url_json_field'] for value_id in url_values
    }
    urls = []
    for id_ in pair_id:
        set_pair = {'location_fk_id': id_[0], 'specialty_fk_id': id_[1]}
        get_url = pair_id_with_urls.get(id_)
        if get_url:
            set_pair['url_json_field'] = pair_id_with_urls.get(id_)
            urls.append(set_pair)
    return urls


unique_pair = get_unique_pair()
url_list = get_pair_id_with_url(unique_pair)


async def execute(task):
    """
    Asynchronous execution of parser functions
    """
    function, location, specialty, url = task
    vacancy_log, error_log = await loop.run_in_executor(None,
                                                        function,
                                                        location,
                                                        specialty,
                                                        url)
    data_for_recording_vacancies.extend(vacancy_log)
    data_for_recording_errors.extend(error_log)

loop = asyncio.get_event_loop()

instruction = [
    (function,
     data['url_json_field'][parser],
     data['location_fk_id'],
     data['specialty_fk_id'])
    for data in url_list for function, parser in parsers
]
tasks = asyncio.wait([loop.create_task(execute(task)) for task in instruction])
loop.run_until_complete(tasks)
loop.close()

for record in data_for_recording_vacancies:
    to_record = Vacancy(**record)
    try:
        to_record.save()
    except DatabaseError:
        pass

if data_for_recording_errors:
    error_dump = Error(error_json_field=data_for_recording_errors)
    error_dump.save()

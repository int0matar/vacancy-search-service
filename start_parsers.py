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

parsers = (
    (work_ua, 'work_ua'),
    (rabota_ua, 'rabota_ua'),
    (dou_ua, 'dou_ua'),
    (djinni_co, 'djinni_co'),
)


def get_unique_pair():
    """
    Returns unique id pairs of tuple by city and language
    """
    subscribed_users = User.objects.filter(is_subscriber=True).values()
    unique_pair_of_user = set(
        (value_id['location_id'], value_id['specialty_id'])
        for value_id in subscribed_users
    )
    return unique_pair_of_user


def get_url(pair_id):
    """
    Returns list with dictionary by unique tuple of get_unique_pair method
    and field UrlAddress.url_data
    """
    url_values = Url.objects.all().values()
    url_dict = {
        (value['location_id'], value['specialty_id']): value['url_json_field']
        for value in url_values
    }
    urls = []
    for pair in pair_id:
        temp = {'location': pair[0], 'specialty': pair[1]}
        url_data = url_dict.get(pair)
        if url_data:
            temp['url_json_field'] = url_dict.get(pair)
            urls.append(temp)
    return urls


unique_pairs = get_unique_pair()
url_list = get_url(unique_pairs)


async def execute(task_pool):
    """
    Asynchronous execution of parser functions
    """
    function, location, specialty, url = task_pool
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
     data['location_fk'],
     data['specialty_fk'])
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

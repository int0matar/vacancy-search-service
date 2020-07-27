import os
import sys
import django
import codecs
import asyncio
from django.db import DatabaseError
from django.contrib.auth import get_user_model
from scraping.models import City, Language, Vacancy, UrlAddress, ErrorLog
from scraping.parsers import *


project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'
django.setup()

User = get_user_model()

jobs_data, errors_data = [], []

parsers = (
    (work_ua, 'work_ua'),
    (rabota_ua, 'rabota_ua'),
    (dou_ua, 'dou_ua'),
    (djinni_co, 'djinni_co'),
)
def get_unique_pair():
    """Returns unique id pairs of tuple by city and language"""
    qset = User.objects.filter(email_subscription=True).values()
    unique_pairs = set((q['city_id'], q['language_id']) for q in qset)
    return unique_pairs

def get_url(id_pairs):
    """Returns list with dictionary by unique tuple of get_unique_pair method
    and field UrlAddress.url_data"""
    qset = UrlAddress.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qset}
    urls = []
    for pair in id_pairs:
        temp = {}
        temp['city'] = pair[0]
        temp['language'] = pair[1]
        temp['url_data'] = url_dict[pair]
        urls.append(temp)
    return urls

unique_pairs = get_unique_pair()
url_list = get_url(unique_pairs)


async def main(value):
"""Asynchronous execution of parser functions"""
    function, url, city, language = value
    job_log, error_log = await loop.run_in_executor(None, function, url,
                                                    city, language)
    jobs_data.extend(job_log)
    errors_data.extend(error_log)

loop = asyncio.get_event_loop()
temp_tasks = [
    (function, data['url_data'][parser], data['city'], data['language'])
    for data in url_list
    for function, parser in parsers
]
tasks = asyncio.wait([loop.create_task(main(temp)) for temp in temp_tasks])
loop.run_until_complete(tasks)
loop.close()


for record in jobs_data:
    record_vacancy = Vacancy(**record)
    try:
        record_vacancy.save()
    except DatabaseError:
        pass

if errors_data:
    error_dump = ErrorLog(error_data=error_log)
    error_dump.save()

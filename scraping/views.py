from django.shortcuts import render

from scraping.models import Vacancy
from scraping.forms import FindForm
from scraping.paginations import *


def home_view(request):
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {
        'city': city,
        'language': language,
    }
    if city or language:
        _request = {}
        if city:
            _request['city__slug'] = city
        if language:
            _request['language__slug'] = language
        filter_list = Vacancy.objects.filter(**_request)

        page_number = request.GET.get('page', 1)
        page_object = get_page_object(filter_list, page_number, 5)
        is_paginated = get_is_paginated(page_object)
        next_url = get_has_next(page_object, city, language)
        prev_url = get_has_previous(page_object, city, language)

        context['object_list'] = page_object
        context['is_paginated'] = is_paginated
        context['next_url'] = next_url
        context['prev_url'] = prev_url
    return render(request, 'scraping/list.html', context)

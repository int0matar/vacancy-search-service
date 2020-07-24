from django.shortcuts import render

from scraping.models import Vacancy
from scraping.forms import FindForm


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
        context['object_list'] = filter_list
    return render(request, 'scraping/list.html', context)

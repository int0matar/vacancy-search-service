from django.shortcuts import render

from scraping.models import Vacancy
from scraping.forms import VacancyRequestForm
from scraping.paginations import (get_page_object, get_paginate, get_next_page,
                                  get_previous_page)


def home_view(request):
    form = VacancyRequestForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    location = request.GET.get('location')
    specialty = request.GET.get('specialty')
    context = {'location': location, 'specialty': specialty}

    if location or specialty:
        request_forms_by_slug = {}
        if location:
            request_forms_by_slug['location__slug'] = location
        if specialty:
            request_forms_by_slug['specialty__slug'] = specialty
        vacancy_filter = Vacancy.objects.filter(**request_forms_by_slug)

        page_number = request.GET.get('page', 1)
        page_object = get_page_object(vacancy_filter, page_number, 5)
        is_paginated = get_paginate(page_object)
        next_url = get_next_page(page_object, location, specialty)
        prev_url = get_previous_page(page_object, location, specialty)

        context['object_list'] = page_object
        context['is_paginated'] = is_paginated
        context['next_url'] = next_url
        context['prev_url'] = prev_url
    return render(request, 'scraping/list.html', context)

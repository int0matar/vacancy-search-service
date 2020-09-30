from django.core.paginator import Paginator


def get_page_object(obj, request_page_number, number_of_page):
    paginator = Paginator(obj, number_of_page)
    page_number = request_page_number
    page_object = paginator.get_page(page_number)
    return page_object


def get_paginate(pagination_obj):
    is_paginated = pagination_obj.has_other_pages()
    return is_paginated


def get_next_page(pagination_obj, location, specialty):
    if pagination_obj.has_next():
        next_url = '?location={}&specialty={}&page={}'.format(
            location,
            specialty,
            pagination_obj.next_page_number())
    else:
        next_url = ''
    return next_url


def get_previous_page(pagination_obj, location, specialty):
    if pagination_obj.has_previous():
        prev_url = '?location={}&specialty={}&page={}'.format(
            location,
            specialty,
            pagination_obj.previous_page_number())
    else:
        prev_url = ''
    return prev_url

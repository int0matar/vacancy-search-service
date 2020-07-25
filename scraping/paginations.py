from django.core.paginator import Paginator


def get_page_object(object, request_page_number, number_of_page):
    paginator = Paginator(object, number_of_page)
    page_number = request_page_number
    page_object = paginator.get_page(page_number)
    return page_object

def get_is_paginated(object):
    is_paginated = object.has_other_pages()
    return is_paginated

def get_has_next(object, city, language):
    if object.has_next():
        next_url = '?city={}&language={}&page={}'.format(
            city,
            language,
            object.next_page_number())
    else:
        next_url = ''
    return next_url

def get_has_previous(object, city, language):
    if object.has_previous():
        prev_url = '?city={}&language={}&page={}'.format(
            city,
            language,
            object.previous_page_number())
    else:
        prev_url = ''
    return prev_url

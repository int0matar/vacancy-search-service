from django import forms

from scraping.models import Location, Specialty


class VacancyRequestForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name='slug',
        required=False,
        label=False,
        empty_label='Выберите локацию',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        to_field_name='slug',
        required=False,
        label=False,
        empty_label='Выберите специальность',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

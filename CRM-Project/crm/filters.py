import django_filters
from django import forms
from .models import Request

OPEN = 'open'
WORK = 'work'
CLOSE = 'close'

STATUS = [
    (OPEN, 'Открыта'),
    (WORK, 'В работе'),
    (CLOSE, 'Закрыта')
]


class FilterRequestsDashboardView(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(
        field_name='status',
        choices=STATUS,
        label=('Статус заявки:')
        )
    specific_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='date',
        widget=forms.SelectDateWidget(),
        label=('Конкретная дата:')
        )
    start_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr=('date__gt'),
        widget=forms.SelectDateWidget(),
        label=('Дата больше чем:')
        )
    end_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr=('date__lt'),
        widget=forms.SelectDateWidget(),
        label=('Дата меньше чем:')
        )

    class Meta:
        model = Request
        fields = ['subject']


class FilterRequestsView(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(
        field_name='status',
        choices=STATUS,
        label=('Статус заявки:')
        )
    specific_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr='date',
        widget=forms.SelectDateWidget(),
        label=('Конкретная дата:')
        )
    start_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr=('date__gt'),
        widget=forms.SelectDateWidget(),
        label=('Дата больше чем:')
        )
    end_date = django_filters.DateFilter(
        field_name='created',
        lookup_expr=('date__lt'),
        widget=forms.SelectDateWidget(),
        label=('Дата меньше чем:')
        )

    class Meta:
        model = Request
        fields = ['status']

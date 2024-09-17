from django.db.models import Q
from django_filters import rest_framework as filters

from tasks.models import Task


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TaskFilter(filters.FilterSet):
    """Filter for Books by if books are published or not"""
    worker = CharFilterInFilter(field_name='worker', method='find_results_maybe_include_null')

    @staticmethod
    def find_results_maybe_include_null(queryset, name, value):
        """
        refactor: filter_params обирает в себя значения в главном цикле
        """
        params_list = []
        filter_params = Q()

        for get_param in value:
            if get_param == 'null':
                params_list.append(Q(**{f'{name}__isnull': True}))
            else:
                params_list.append(Q(**{name: get_param}))

        for param in params_list:
            if filter_params == Q():
                filter_params = param
                continue

            filter_params = filter_params | param

        return queryset.filter(filter_params)

    class Meta:
        model = Task
        fields = ['worker', 'customer', 'status']

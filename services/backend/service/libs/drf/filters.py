from django_filters.rest_framework import filters, FilterSet


class BaseFromToFilterSet(FilterSet):
    timestamp_from = filters.DateTimeFilter(lookup_expr='gte', method='filter_from_timestamp')
    timestamp_to = filters.DateTimeFilter(lookup_expr='lte', method='filter_to_timestamp')

    def filter_from_timestamp(self, qs, field_name, value):
        return qs.filter(
            created_at__gte=self.request.GET.get(field_name))

    def filter_to_timestamp(self, qs, field_name, value):
        return qs.filter(
            created_at__lte=self.request.GET.get(field_name))

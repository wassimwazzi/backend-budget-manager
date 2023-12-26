from rest_framework import viewsets
from .serializers import CurrencySerializer
from .models import Currency


class CurrencyView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CurrencySerializer
    pagination_class = None

    def get_queryset(self):
        """ """
        return Currency.objects.all()

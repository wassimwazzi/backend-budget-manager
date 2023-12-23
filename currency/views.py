from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import CurrencySerializer
from .models import Currency


class CurrencyView(viewsets.ModelViewSet):
    serializer_class = CurrencySerializer

    def get_queryset(self):
        """
        This view should return a list of all the transactions
        for the currently authenticated user.
        """
        return Currency.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        paginate = self.request.query_params.get("paginate", None)
        # If paginate is false, return all categories
        if paginate == "false":
            serializer = CurrencySerializer(queryset, many=True)
            return Response(serializer.data)
        # If paginate is true, return paginated categories
        page = self.paginate_queryset(queryset)
        serializer = CurrencySerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

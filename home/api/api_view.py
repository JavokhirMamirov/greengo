from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *


class CustomViewSet(viewsets.ModelViewSet):
    serializer_class__related = None

    def get_serializer_related(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class_related()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class_related(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class__related is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.serializer_class__related

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            headers = self.get_success_headers(serializer.data)
            if self.serializer_class__related is not None:
                serializer = self.get_serializer_related(obj)
            data = {
                "success": True,
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
            return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            if self.serializer_class__related is not None:
                serializer = self.get_serializer_related(queryset, many=True)
            else:
                serializer = self.get_serializer(queryset, many=True)
            data = {
                "success": True,
                "data": serializer.data
            }
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if self.serializer_class__related is not None:
                serializer = self.get_serializer_related(instance)
            else:
                serializer = self.get_serializer(instance)
            data = {
                "success": True,
                "data": serializer.data
            }
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
        return Response(data)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            if self.serializer_class__related is not None:
                serializer = self.get_serializer_related(obj)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            data = {
                "success": True,
                "data": serializer.data
            }
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }

        return Response(data)


class DispatcherViewset(CustomViewSet):
    serializer_class = DispatcherSerializer
    queryset = Dispatcher.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active',)


class BoardViewset(CustomViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active',)


class OwnerOperatorViewset(CustomViewSet):
    serializer_class = OwnerOperatorSerializer
    queryset = OwnerOperator.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active',)


class DriverViewset(CustomViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active',)


class InvoiceViewset(CustomViewSet):
    serializer_class = InvoiceSerializer
    serializer_class__related = InvoiceRelatedSerializer
    queryset = Invoice.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        'date': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }
    search_fields = ('disptacher__name', 'driver__name')
    filter_fields = ('dispatcher', 'driver')

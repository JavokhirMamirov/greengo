from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import *


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def login(request):
    try:
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            user = User.objects.get(username=username)
            ps = make_password(password)
            if user.check_password(password):
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                dt = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "token": token.key
                }
                data = {
                    "success": True,
                    "status": 200,
                    "data": dt
                }
            else:
                data = {
                    "success": False,
                    "status": 403,
                    "error": "Password error!"
                }

        except User.DoesNotExist as err:
            data = {
                "success": False,
                "status": 404,
                "error": "{}".format(err)
            }
    except Exception as err:
        data = {
            "success": False,
            "status": 500,
            "error": "{}".format(err)
        }
    return Response(data)


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
        'dispatcher': ['exact'],
        'driver': ['exact'],
        'board': ['exact'],
        'owner': ['exact'],
        'status': ['exact'],
    }
    search_fields = ('dispatcher__name', 'driver__name', 'owner__name')


class InvoiceStatusViewset(CustomViewSet):
    serializer_class = InvoiceStatusSerializer
    queryset = InvoiceStatus.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active',)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def pdf_file(request):
    if request.method == "GET":
        try:
            invoice_id = request.GET.get('invoice_id')
            invoice = Invoice.objects.get(id=invoice_id)
            ser = PdfFileSerializers(invoice.documents.all(), many=True)
            data = {
                "success": True,
                "data": ser.data
            }
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
        return Response(data)
    elif request.method == "POST":
        try:
            file = request.data['file']
            invoice_id = request.data.get('invoice_id')
            invoice = Invoice.objects.get(id=invoice_id)
            pdf = PdfFile.objects.create(
                file=file
            )
            invoice.documents.add(pdf)
            invoice.save()
            ser = PdfFileSerializers(pdf)
            data = {
                "success": True,
                "data": ser.data
            }
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
        return Response(data)
    elif request.method == "PUT":
        try:
            file = request.data['file']
            file_id = request.data.get('file_id')
            pdf = PdfFile.objects.get(id=file_id)
            pdf.file = file
            pdf.save()
            ser = PdfFileSerializers(pdf)
            data = {
                "success": True,
                "data": ser.data
            }
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
        return Response(data)
    else:
        try:
            file_id = request.data.get('file_id')
            invoice_id = request.data.get('invoice_id')
            pdf = PdfFile.objects.get(id=file_id)
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.documents.remove(pdf)
            invoice.save()
            data = {
                "success": True,
                "data": {
                    "file_id": file_id
                }
            }
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
        return Response(data)

from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import *
from ..models import Documents


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
            # mutable = request.data._mutable
            # request.data._mutable = True
            request.data['company'] = request.user.id
            # request.data._mutable = mutable
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
            queryset = queryset.filter(company_id=request.user.id)

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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            data = {
                "success": True,
                "data": "Instance Deleted!"
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
    http_method_names = ['get', "post", "put"]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active',)


class BoardViewset(CustomViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    http_method_names = ['get', "post", "put"]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active',)


class OwnerOperatorViewset(CustomViewSet):
    serializer_class = OwnerOperatorSerializer
    queryset = OwnerOperator.objects.all()
    http_method_names = ['get', "post", "put"]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active',)


class DriverViewset(CustomViewSet):
    serializer_class = DriverSerializer
    serializer_class__related = DriverWithStatusSerializer
    queryset = Driver.objects.all()
    http_method_names = ['get', "post", "put"]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('is_active', 'status')


class InvoiceViewset(CustomViewSet):
    serializer_class = InvoiceSerializer
    serializer_class__related = InvoiceRelatedSerializer
    queryset = Invoice.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        'date': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'trip_rate': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'dispatcher': ['exact'],
        'driver': ['exact'],
        'board': ['exact'],
        'owner': ['exact'],
        'status': ['exact'],
    }
    search_fields = ('dispatcher__name', 'driver__name', 'owner__name', 'origin', 'destination')

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            boards = Board.objects.filter(is_active=True)
            data_t = []
            for board in boards:

                t_gross = 0
                for data in response.data['data']:
                    if data['board']['id'] == board.id:
                        t_gross += float(data.get('trip_rate', 0))
                dt = {
                    "id": board.id,
                    "name": board.name,
                    "gross": t_gross
                }
                data_t.append(dt)

            total_gross = sum([float(data.get('trip_rate', 0)) for data in response.data['data']])
            total_mile = sum([float(data.get('milage', 0)) for data in response.data['data']])
            total_hd = sum([float(data.get('dh', 0)) for data in response.data['data']])
            response.data['total_miles'] = total_mile + total_hd
            response.data['total_gross'] = total_gross
            if total_mile + total_hd > 0:
                response.data['total_average'] = round(total_gross / (total_mile + total_hd), 2)
            else:
                response.data['total_average'] = 0

            response.data['board_data'] = data_t
            return response
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
            return data


class InvoiceStatusViewset(CustomViewSet):
    serializer_class = InvoiceStatusSerializer
    queryset = InvoiceStatus.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    http_method_names = ['get', "post", "put"]
    search_fields = ('name',)
    filter_fields = ('is_active',)


class DriverStatusViewset(CustomViewSet):
    serializer_class = DriverStatusSerializer
    queryset = DriverStatus.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    http_method_names = ['get', "post", "put"]
    search_fields = ('name',)
    filter_fields = ('is_active',)


@api_view(['POST'])
def delete_pdf(request):
    try:
        file_id = request.data['file_id']
        invoice_id = request.data.get('invoice_id')
        pdf = PdfFile.objects.get(id=file_id)
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.documents.remove(pdf)
        invoice.save()
        pdf.delete()
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

@api_view(['POST'])
def delete_doc_file(request):
    try:
        file_id = request.data.get('file_id')
        doc_id = request.data.get('doc_id')
        pdf = PdfFile.objects.get(id=file_id)
        doc = Documents.objects.get(id=doc_id)
        doc.file.remove(pdf)
        doc.save()
        pdf.delete()
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
                file=file,
                name=file.name
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
    elif request.method == "DELETE":
        try:
            # file_id = request.data['file_id']
            file_id = 1
            # invoice_id = request.POST['invoice_id']
            # pdf = PdfFile.objects.get(id=file_id)
            # invoice = Invoice.objects.get(id=invoice_id)
            # invoice.documents.remove(pdf)
            # invoice.save()
            # pdf.delete()
            data = {
                "success": True,
                "data": {
                    "file_id": f"{request.DELETE}"
                }
            }
        except Exception as err:
            data = {
                "success": False,
                "error": "{}".format(err)
            }
        return Response(data)


class DocumentsViewset(CustomViewSet):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
    serializer_class__related = DocumentsManySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    filter_fields = ('type',)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def document_file(request):
    if request.method == "GET":
        try:
            doc_id = request.GET.get('doc_id')
            doc = Documents.objects.get(id=doc_id)
            ser = PdfFileSerializers(doc.file.all(), many=True)
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
            doc_id = request.data.get('doc_id')
            doc = Documents.objects.get(id=doc_id)
            pdf = PdfFile.objects.create(
                file=file,
                name=file.name

            )
            doc.file.add(pdf)
            doc.save()
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
            doc_id = request.data.get('doc_id')
            pdf = PdfFile.objects.get(id=file_id)
            doc = Documents.objects.get(id=doc_id)
            doc.file.remove(pdf)
            doc.save()
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


@api_view(["GET"])
def Preformance(request):
    try:
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        invoices = Invoice.objects.filter(
            date__date__gte=date_start,
            date__date__lte=date_end
        )
        dispatecher_preformance = []
        driver_preformance = []
        board_preformance = []

        dispatchers = Dispatcher.objects.filter(is_active=True)
        boards = Board.objects.filter(is_active=True)
        drivers = Driver.objects.filter(is_active=True)

        for board in boards:
            trip_all_rate = invoices.filter(board=board).aggregate(total=Sum('trip_rate')).get('total')
            if trip_all_rate is None:
                trip_all_rate = 0

            dt = {
                "board": board.name,
                "summa": trip_all_rate
            }
            board_preformance.append(dt)

        for dispatcher in dispatchers:
            total_milage = invoices.filter(dispatcher=dispatcher).aggregate(total=Sum('milage')).get('total')
            total_dh = invoices.filter(dispatcher=dispatcher).aggregate(total=Sum('dh')).get('total')
            total_trip_rate = invoices.filter(dispatcher=dispatcher).aggregate(total=Sum('trip_rate')).get('total')
            if total_milage is None:
                total_milage = 0
            if total_dh is None:
                total_dh = 0
            if total_trip_rate is None:
                total_trip_rate = 0

            miles = total_milage + total_dh
            if miles != 0:
                avrage = total_trip_rate / miles
            else:
                avrage = 0

            dt_dis = {
                "name": dispatcher.name,
                "miles": miles,
                "gross": total_trip_rate,
                "avrage": round(avrage, 2)
            }
            dispatecher_preformance.append(dt_dis)

        for driver in drivers:
            total_milage = invoices.filter(driver=driver).aggregate(total=Sum('milage')).get('total')
            total_dh = invoices.filter(driver=driver).aggregate(total=Sum('dh')).get('total')
            total_trip_rate = invoices.filter(driver=driver).aggregate(total=Sum('trip_rate')).get('total')
            if total_milage is None:
                total_milage = 0
            if total_dh is None:
                total_dh = 0
            if total_trip_rate is None:
                total_trip_rate = 0

            miles = total_milage + total_dh
            if miles != 0:
                avrage = total_trip_rate / miles
            else:
                avrage = 0

            dt_driv = {
                "name": driver.name,
                "miles": miles,
                "gross": total_trip_rate,
                "avrage": round(avrage, 2)
            }
            driver_preformance.append(dt_driv)
        data = {
            "board": board_preformance,
            "dispatcher": dispatecher_preformance,
            "driver": driver_preformance
        }

    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)


@api_view(["POST"])
def DriverActivity(request):
    try:
        status = request.data['status']
        driver_id = request.data['driver']
        dv_status = DriverStatus.objects.get(id=status)
        dv = Driver.objects.get(id=driver_id)
        dv.status = dv_status
        dv.save()
        data = {
            "success": True,
            "data": DriverWithStatusSerializer(dv).data
        }
    except Exception as err:
        data = {
            "success": False,
            "error": "{}".format(err)
        }
    return Response(data)

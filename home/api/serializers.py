from rest_framework import serializers

from ..models import Dispatcher, Board, OwnerOperator, Driver, Invoice, InvoiceStatus, PdfFile, Documents, DriverStatus


class DispatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatcher
        fields = '__all__'

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"
        read_only_fields = ['file', ]

class PdfFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = PdfFile
        fields = "__all__"


class DocumentsManySerializer(serializers.ModelSerializer):
    file = PdfFileSerializers(many=True, read_only=True)
    class Meta:
        model = Documents
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class OwnerOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerOperator
        fields = '__all__'

class DriverStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverStatus
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class DriverWithStatusSerializer(serializers.ModelSerializer):
    status = DriverStatusSerializer(read_only=True)
    owner = OwnerOperatorSerializer(read_only=True)
    destination = serializers.SerializerMethodField()
    class Meta:
        model = Driver
        fields = [
            "id",
            "company",
            "owner",
            "name",
            "phone",
            "trailer_number",
            "track_number",
            "email",
            "status",
            "is_active",
            "update_time",
            "destination",
        ]

    def get_destination(self, obj):
        inv = Invoice.objects.filter(driver=obj).last()
        if inv is not None:
            return inv.destination
        else:
            return None


class InvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceStatus
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['documents', ]






class InvoiceRelatedSerializer(serializers.ModelSerializer):
    dispatcher = DispatcherSerializer(read_only=True)
    board = BoardSerializer(read_only=True)
    owner = OwnerOperatorSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    status = InvoiceStatusSerializer(read_only=True)
    documents = PdfFileSerializers(read_only=True, many=True)



    class Meta:
        model = Invoice
        fields = '__all__'


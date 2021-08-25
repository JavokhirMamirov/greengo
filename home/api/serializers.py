from rest_framework import serializers

from ..models import Dispatcher, Board, OwnerOperator, Driver, Invoice, InvoiceStatus, PdfFile


class DispatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatcher
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class OwnerOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerOperator
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class InvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceStatus
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class PdfFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = PdfFile
        fields = "__all__"

class InvoiceRelatedSerializer(serializers.ModelSerializer):
    dispatcher = DispatcherSerializer(read_only=True)
    board = BoardSerializer(read_only=True)
    owner = OwnerOperatorSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    status = InvoiceStatusSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'



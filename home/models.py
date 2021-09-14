from django.db import models


# Create your models here.


class Dispatcher(models.Model):
    name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Board(models.Model):
    name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class OwnerOperator(models.Model):
    name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    trailer_number = models.IntegerField(default=0)
    track_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class InvoiceStatus(models.Model):
    name = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=25, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PdfFile(models.Model):
    file = models.FileField(upload_to='pdf/', null=True, blank=True)


class Invoice(models.Model):
    dispatcher = models.ForeignKey(Dispatcher, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    owner = models.ForeignKey(OwnerOperator, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    dh = models.DecimalField(default=0, decimal_places=3, max_digits=10)
    origin = models.CharField(max_length=255)
    milage = models.DecimalField(default=0, decimal_places=3, max_digits=10)
    destination = models.CharField(max_length=255)
    trip_rate = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    notes = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(null=True, blank=True)
    documents = models.ManyToManyField(PdfFile)
    status = models.ForeignKey(
        InvoiceStatus, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.board.name


class Documents(models.Model):
    types = (
        (1, "Documents"),
        (2, "Drivers Aplications"),
        (3, "Existiong Trucks Docs")
    )

    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.ManyToManyField(PdfFile)
    type = models.IntegerField(default=1, choices=types)

    def __str__(self):
        return self.name

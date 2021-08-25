from django.urls import path, include

from .api_view import login, pdf_file
from .router import router

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login),
    path('pdf-file/', pdf_file)
]

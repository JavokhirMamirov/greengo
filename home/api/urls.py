from django.urls import path, include

from .api_view import login
from .router import router

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login)
]

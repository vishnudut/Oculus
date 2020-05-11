from django.urls import path, include
from . import views, faceEncodings


urlpatterns = [
    path('compareFaces', views.compareFaces, name="compareFaces"),
    path('encoding', faceEncodings.encoding, name="faceEncoding")
]

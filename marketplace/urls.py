from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.home, name="home"),
    path("trade/", views.trade, name="trade"),
    path("marketplace/", views.marketplace, name="marketplace"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
]

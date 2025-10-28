from django.urls import path
from .views import (
    login_view,
    register_user,
    supplier_dashboard_view,
    buyer_dashboard_view,
    home_view,
)

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("supplier-dashboard/", supplier_dashboard_view, name="supplier-dashboard"),
    path("buyer-dashboard/", buyer_dashboard_view, name="buyer-dashboard"),
    path("", home_view, name="home"),
]

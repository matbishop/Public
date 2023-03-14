from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("calculator/", views.calculator, name="calculator"),
    path("currency/", views.currency, name="currency"),
    path("shares/", views.shares, name="shares"),
    path("transactions/", views.transactions, name="transactions"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("delete/", views.delete_transaction, name="delete_transaction"),
]
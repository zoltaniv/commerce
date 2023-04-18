from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_auction", views.new_auction, name="new_auction"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:category_id>/", views.category, name="category"),
    path("categories/<int:category_id>/<int:auction_id>", views.auction_view, name="auction_view")]

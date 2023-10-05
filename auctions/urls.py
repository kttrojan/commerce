from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.view_category, name="view_category"),
    path("<int:listing_id>", views.view_listing, name="view_listing"),
    path("watchlist_add/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:listing_id>", views.watchlist_remove, name="watchlist_remove"),
    path("watchlists", views.watchlists, name="watchlists"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("add_bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
]


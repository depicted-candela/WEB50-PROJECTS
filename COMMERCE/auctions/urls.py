from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("category/", views.category, name="category"),
    path("category/<str:id>", views.category_l, name="category_l"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("auction/<str:id>", views.auction, name="auction"),
    path("auction/<str:id>/watch", views.watch_auction, name="watch_auction"),
    path("auction/<str:id>/bid", views.bid_auction, name="bid_auction"),
    path("auction/<str:id>/close", views.close_auction, name="close_auction"),
    path("comment/<str:id>", views.comment_auction, name="comment_auction"),
    path("comment/<str:id>/cancel", views.cancel_comment_auction, name="cancel_comment_auction"),
    path("watchlist/", views.watchlist, name="watchlist")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

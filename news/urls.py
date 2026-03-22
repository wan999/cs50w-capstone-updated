from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login_view", views.login_view, name="login"),
    path("logout_view", views.logout_view, name="logout"),
    path("<str:username>/profile", views.profile, name="profile"),
    path("<str:username>/edit_profile", views.edit_profile, name="edit_profile"),
    path("create_article", views.create_article, name="create_article"),
    path("search", views.search, name="search"),
    path("<str:article_title>", views.single_post, name="single_post"),
    path("<str:article_title>/delete", views.delete_article, name="delete_article"),
    path("category/<str:category>", views.filter_articles, name="filter_articles"),
    path("<int:article_id>/comments", views.add_comment, name="add_comment"),
    path("<int:article_id>/add_to_favorites", views.add_to_favorites, name="add_to_favorites"),
    path("<str:article_title>/delete_favorite", views.delete_favorite, name="delete_favorite"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

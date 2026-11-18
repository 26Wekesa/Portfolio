from django.contrib import admin
from django.urls import path

from core import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.page, {"template_name": "index.html"}, name="home"),
    path("index.html", views.page, {"template_name": "index.html"}, name="home-file"),
    path("about.html", views.page, {"template_name": "about.html"}, name="about"),
    path("resume.html", views.page, {"template_name": "resume.html"}, name="resume"),
    path("services.html", views.page, {"template_name": "services.html"}, name="services"),
    path("portfolio.html", views.page, {"template_name": "portfolio.html"}, name="portfolio"),
    path("contact.html", views.page, {"template_name": "contact.html"}, name="contact"),
    path(
        "portfolio-details.html",
        views.page,
        {"template_name": "portfolio-details.html"},
        name="portfolio-details",
    ),
    path(
        "service-details.html",
        views.page,
        {"template_name": "service-details.html"},
        name="service-details",
    ),
    path(
        "starter-page.html",
        views.page,
        {"template_name": "starter-page.html"},
        name="starter-page",
    ),
    path("forms/contact/", views.submit_contact, name="contact_submit"),
]

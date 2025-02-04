from django.urls import path, include

urlpatterns = [
    path("api/", include("app.urls")),  # Include the study API URLs
]
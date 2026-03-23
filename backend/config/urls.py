from django.http import JsonResponse
from django.urls import path
from ninja import NinjaAPI

from alerts.api import router

api = NinjaAPI(title="Multi-tenant Alerts API")
api.add_router("/", router)


def health(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", health),
    path("api/", api.urls),
]

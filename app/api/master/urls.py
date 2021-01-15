from django.urls import path, include
from .views import MasterListView, MasterBookedHoursView, WorkTypesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'work-types', WorkTypesViewSet)

urlpatterns = [
    path('masters/', MasterListView.as_view()),
    path('masters/<int:pk>/', MasterBookedHoursView.as_view()),
    path('', include(router.urls)),
]

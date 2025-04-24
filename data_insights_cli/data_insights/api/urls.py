from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetAnalysisView, DatasetViewSet, PredictView

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
    path('datasets/<int:pk>/analyze/', DatasetAnalysisView.as_view(), name='dataset-analyze'),
    path('datasets/<int:pk>/predict/', PredictView.as_view(), name='dataset-predict'),
]
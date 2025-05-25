from django.urls import path
from resources.api.views import ResourceListCreateView, ResourceRetrieveUpdateDestroyView, ResourceDownloadView

urlpatterns = [
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
    path('resources/<int:pk>/', ResourceRetrieveUpdateDestroyView.as_view(), name='resource-detail'),
    path('resources/download/<int:pk>/', ResourceDownloadView.as_view(), name='resource-download'),
]

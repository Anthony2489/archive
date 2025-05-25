from rest_framework import generics, permissions, filters
from resources.models import resources as ResourceModel
from student.models import Student
from custom.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse, Http404
import os
from .serializers import ResourceSerializer
from rest_framework import status
from django.urls import reverse

# Permissions
class IsLecturerOrClassRep(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['lecture', 'cr']

# CRUD Views
class ResourceListCreateView(generics.ListCreateAPIView):
    """
    List all resources (GET) or create a new resource (POST, only for lecturers/class reps).
    Supports filtering, searching, and ordering.
    """
    queryset = ResourceModel.objects.filter(is_active=True)
    serializer_class = ResourceSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['uploaded_at', 'resource_type']
    search_fields = ['resource_type', 'course_id__course_name', 'assignment__title']
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturerOrClassRep()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class ResourceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a resource by ID.
    Update/delete only allowed for lecturers/class reps.
    """
    queryset = ResourceModel.objects.all()
    serializer_class = ResourceSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturerOrClassRep()]
        return [permissions.IsAuthenticated()]

class ResourceDownloadView(APIView):
    """
    Download a resource file by ID. Only for authenticated users.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            resource = ResourceModel.objects.get(pk=pk, is_active=True)
            if not resource.resource_file:
                raise Http404
            file_path = resource.resource_file.path
            file_handle = open(file_path, 'rb')
            response = FileResponse(file_handle, as_attachment=True, filename=os.path.basename(file_path))
            return response
        except ResourceModel.DoesNotExist:
            raise Http404
        except Exception:
            raise Http404 
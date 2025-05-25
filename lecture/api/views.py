import json
from django.http import JsonResponse, FileResponse, Http404
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import (
    exceptions as rest_exceptions,
    response,
    viewsets,
    decorators as rest_decorators,
    permissions as rest_permissions,
)
from resources.models import Assignments, AssignmentSubmissions, resources
from .serializers import UserSerializer, LectureSerializer, UpdateSerializer, AssignmentSerializer, AssignmentSubmissionSerializer, ResourceSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import os


def get_csrf(request):
    response = JsonResponse(
        {"Info": "Success - Set CSRF cookie", "Token": get_token(request)}
    )
    response["X-CSRFToken"] = get_token(request)
    token = get_token(request)

    print(token)
    return response


@ensure_csrf_cookie
def check_auth(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})

    return JsonResponse({"isAuthenticated": True})


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.AllowAny])
def loginView(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return JsonResponse({"Info": "Email and Password are needed"}, status=400)

    try:
        user_obj = User.objects.get(email__iexact=email)  # Case-insensitive
    except User.DoesNotExist:
        return JsonResponse({"Info": "User with given credentials does not exist"}, status=400)

    user = authenticate(request, username=user_obj.username, password=password)

    if user is None:
        return JsonResponse({"Info": "Incorrect password"}, status=400)

    login(request, user)
    return JsonResponse({"user": UserSerializer(user).data, "Info": "User logged in successfully"})


def logoutView(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You're not logged in"}, status=400)

    logout(request)
    return JsonResponse({"detail": "Successfully logged out"})


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    @staticmethod
    def get(request, format=None):
        print(request.user.username)
        user = request.user
        data = {
            'full_name': user.first_name,
            'username': user.username,
            'email': user.email,
            # 'department': user.department
        }
        return JsonResponse(data, safe=False)


class LectureView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(detail=False, methods=['GET'])
    def by_username(self, request):
        username = request.query_params.get('username')
        user = User.objects.get(username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class LectureOnlyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response({"user": user.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Something went wrong when trying to load user"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.AllowAny])
# @method_decorator(csrf_protect, name='dispatch')
def registerView(request):
    serializer = LectureSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response(
            {
                "user": UserSerializer(user).data,
                "message": "Account created successfully",
            }
        )

    return rest_exceptions.AuthenticationFailed("Invalid credentials!")


@rest_decorators.api_view(['PUT', 'PATCH'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def update_account(request):
    user = request.user
    serializer = UpdateSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@rest_decorators.api_view(['DELETE'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class IsLecturer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'lecture'


# Assignment CRUD
class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['due_date', 'created_at']
    search_fields = ['title', 'course_id__course_name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturer()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Only assignments created by this lecturer
        return Assignments.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AssignmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    queryset = Assignments.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturer()]
        return [permissions.IsAuthenticated()]


# Assignment Submissions (view and feedback)
class AssignmentSubmissionListView(generics.ListAPIView):
    serializer_class = AssignmentSubmissionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['submission_date']
    search_fields = ['student__user__username', 'assignment__title']
    permission_classes = [IsLecturer]

    def get_queryset(self):
        # All submissions for assignments created by this lecturer
        return AssignmentSubmissions.objects.filter(assignment__created_by=self.request.user)


class AssignmentSubmissionFeedbackView(generics.UpdateAPIView):
    serializer_class = AssignmentSubmissionSerializer
    queryset = AssignmentSubmissions.objects.all()
    permission_classes = [IsLecturer]
    http_method_names = ['patch']


# Resource CRUD
class ResourceListCreateView(generics.ListCreateAPIView):
    serializer_class = ResourceSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['uploaded_at', 'resource_type']
    search_fields = ['resource_type', 'course_id__course_name', 'assignment__title']
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsLecturer()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return resources.objects.filter(uploaded_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class ResourceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResourceSerializer
    queryset = resources.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsLecturer()]
        return [permissions.IsAuthenticated()]


class ResourceDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            resource = resources.objects.get(pk=pk)
            if not resource.resource_file:
                raise Http404
            file_path = resource.resource_file.path
            file_handle = open(file_path, 'rb')
            response = FileResponse(file_handle, as_attachment=True, filename=os.path.basename(file_path))
            return response
        except resources.DoesNotExist:
            raise Http404
        except Exception:
            raise Http404

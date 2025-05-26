from django.urls import path
from rest_framework.routers import DefaultRouter
from custom.api.views import UserListView, UserProfileView, user_role_view

urlpatterns = []
router = DefaultRouter()
router.register('user', UserListView, basename='user')
urlpatterns += router.urls

urlpatterns += [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('role/', user_role_view, name='user-role'),
]
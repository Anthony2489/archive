from django.urls import path
from .views import (
    registerView,
    get_csrf,
    loginView,
    WhoAmIView,
    StudentOnlyView,
    check_auth,
    logoutView,
    getSession,
    update_account,
    delete_account,
    StudentAssignmentSubmissionListCreateView,
    StudentAssignmentSubmissionDetailView,
    StudentResourceListView,
    ResourceDownloadView,
)

urlpatterns = [
    path("sessionId", getSession.as_view()),
    path("csrf_cookie", get_csrf),
    path("check_auth", check_auth),
    path("register", registerView),
    path("login", loginView),
    path("get_user", WhoAmIView.as_view()),
    path("student_dashboard", StudentOnlyView.as_view()),
    path("logout", logoutView),
    path("update", update_account),
    path("delete", delete_account),
    path('submissions/', StudentAssignmentSubmissionListCreateView.as_view(), name='student-submission-list-create'),
    path('submissions/<int:pk>/', StudentAssignmentSubmissionDetailView.as_view(), name='student-submission-detail'),
    path('resources/', StudentResourceListView.as_view(), name='student-resource-list'),
    path('resources/download/<int:pk>/', ResourceDownloadView.as_view(), name='student-resource-download'),
]

from django.urls import path

from portal.views import teacher_views

app_name = 'portal'

urlpatterns = [
    path('', teacher_views.TeacherListView.as_view(), name='teachers'),
    path('create/', teacher_views.TeacherCreateView.as_view(), name='teacher-create'),
    path(
        '<int:pk>/contact-create/',
        teacher_views.TeacherCreateAddressView.as_view(),
        name='teacher-contact-create'
    ),
    path('<int:pk>/', teacher_views.TeacherDetailView.as_view(),
            name='teacher-detail'),
    path('<int:pk>/edit/', teacher_views.TeacherUpdateView.as_view(),
            name='teacher-edit'),
    path('archived/', teacher_views.TeacherArchiveView.as_view(),
            name='teachers-archived'),
]

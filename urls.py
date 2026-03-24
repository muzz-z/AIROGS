from django.urls import path
from . import views

urlpatterns = [
    # User / Doctor flow
    path('', views.detect_glaucoma, name='detect'),
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('upload/', views.upload_image, name='upload'),
    path('results/', views.results, name='results'),

    # Admin flow
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/user/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('admin/user/activate/<int:user_id>/', views.activate_user, name='activate_user'),
    path('admin/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]

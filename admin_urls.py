from django.urls import path
from .views import (
    admin_dashboard,
    activate_user,
    deactivate_user,
    delete_user,
)

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),

    path('user/activate/<int:user_id>/', activate_user, name='activate_user'),
    path('user/deactivate/<int:user_id>/', deactivate_user, name='deactivate_user'),
    path('user/delete/<int:user_id>/', delete_user, name='delete_user'),
]

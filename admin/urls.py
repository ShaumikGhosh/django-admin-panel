from django.urls import path
from admin.views import *



urlpatterns = [
    path('admin/', admin),
    path('admin/login/', AdminDashboardLogin.as_view(), name='login'),
    path('admin/dashboard/', AdminDashboardIndex.as_view(), name='index'),
    path('admin/logout/', AdminDashboardLogout.as_view(), name='logout'),
    path('admin/settings/', AdminDashboardSettings.as_view(), name='settings'),
]
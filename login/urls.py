from django.urls import path
from login import views
app_name="login"
urlpatterns = [
    path('', views.index, name="index"),
    path('verify', views.login_verify, name="verify"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.user_logout, name="logout"),
    path('websocket-start', views.websocket_start, name="websocket_start"),
]
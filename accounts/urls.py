from django.urls import path

from accounts.views import (
    register_view, login_view, account_view, logout_view, update_view,
    delete_view
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('account/', account_view, name='account'),
    path('logout/', logout_view, name='logout'),
    path('update/', update_view, name='update'),
    path('delete/', delete_view, name='delete'),
]

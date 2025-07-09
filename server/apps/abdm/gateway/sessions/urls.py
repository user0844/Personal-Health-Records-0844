from django.urls import path
from .views import GetABDMSessionView, CreateABDMSessionView, RefreshABDMSessionView

urlpatterns = [
    path('get/', GetABDMSessionView.as_view(), name='get_abdm_session'),
    path('create/', CreateABDMSessionView.as_view(), name='create_abdm_session'),
    path('refresh/', RefreshABDMSessionView.as_view(), name='refresh_abdm_session'),
] 
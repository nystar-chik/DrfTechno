from django.urls import path
from account.views import Register, Login, ProfileAPIView, VerifyCode, Resetpass, VerifyCodePassword

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('verify-otp/', VerifyCode.as_view()),
    path('reset-password/', Resetpass.as_view()),
    path('reset-password/verify/', VerifyCodePassword.as_view())
]
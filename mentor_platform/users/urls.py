# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MentorViewSet, MenteeViewSet, FeedbackViewSet, MentorSignUpView, MenteeSignUpView
from .views import SignUpView, CustomAuthToken, LogoutView
from .views import EmailVerificationView, FeedbackCreateView
from .views import CustomAuthToken, RequestOTP

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'mentors', MentorViewSet)
router.register(r'mentees', MenteeViewSet)
router.register(r'feedbacks', FeedbackViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpView.as_view(), name='signup'),
    
    path('signup/mentor/', MentorSignUpView.as_view(), name='mentorsignup'),
    path('signup/mentee/', MenteeSignUpView.as_view(), name='menteesignup'),
    
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('api/verify-email/<str:token>/', EmailVerificationView.as_view(), name='verify_email'),

    path('post/feedback/', FeedbackCreateView.as_view(), name='post-feedback'),

    path('api/token/', CustomAuthToken.as_view(), name='custom_auth_token'),
    path('api/request-otp/', RequestOTP.as_view(), name='request_otp'),
    
]


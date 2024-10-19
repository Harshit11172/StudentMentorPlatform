#views.py

from rest_framework import viewsets
from .models import Mentor, Mentee, Feedback
from voice_video.models import Booking
from .serializers import MentorSerializer, MenteeSerializer, FeedbackSerializer, MentorSignupSerializer, MenteeSignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

#-------------login-Logout-Signup----------------------------------

from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer  # Create this serializer
from rest_framework import status
from users.utils import send_otp_email  # You need to implement this
from users.models import OTP  # A model to store OTPs if needed
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from users.models import OTP  # Ensure this import is present
from users.utils import send_otp_email  # Implement this function to send OTPs



User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer  # Serializer to handle user creation
    permission_classes = [permissions.AllowAny]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'error': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the OTP is valid
        try:
            otp_instance = OTP.objects.get(user=user, code=otp, is_verified=False)
            # Mark the OTP as verified
            otp_instance.is_verified = True
            otp_instance.save()

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid email or OTP.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({
            'message': 'Send a POST request with "email" and "otp" to login.',
            'example': {
                'email': 'your_email@example.com',
                'otp': '123456'
            }
        }, status=status.HTTP_200_OK)

    def send_otp(self, user):
        otp_code = get_random_string(length=6, allowed_chars='0123456789')  # Generate a random OTP
        OTP.objects.create(user=user, code=otp_code)  # Store the OTP in the database
        send_otp_email(user.email, otp_code)  # Send the OTP via email


class RequestOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            # Generate OTP
            otp_code = get_random_string(length=6, allowed_chars='0123456789')
            OTP.objects.create(user=user, code=otp_code)  # Save OTP to the database
            send_otp_email(user.email, otp_code)  # Send the OTP email

            return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
    
#     def get(self, request, *args, **kwargs):
#         return Response({
#             'message': 'Send a POST request with "username" and "password" to login.',
#             'example': {
#                 'username': 'your_username',
#                 'password': 'your_password'
#             }
#         }, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."})

##-----------------------------------------------------------------

class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [AllowAny]

class MenteeViewSet(viewsets.ModelViewSet):
    queryset = Mentee.objects.all()
    serializer_class = MenteeSerializer
    # permission_classes = [AllowAny]

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user
        print(f"User: {user.username}, User Type: {user.user_type}")

        if user.user_type != 'mentee':
            raise ValueError("User is not a mentee.")

        print(self.request.user.mentee_profile)

        try:
            mentee = user.mentee_profile

            # Get mentor from the request data
            mentor = self.request.data.get('mentor')
            if not mentor:
                raise ValidationError("Mentor ID is required.")

            try:
                mentor = Mentor.objects.get(id=mentor)
            except Mentor.DoesNotExist:
                raise ValidationError("Mentor not found.")

            # Check for completed bookings associated with the mentee and mentor
            completed_bookings = Booking.objects.filter(mentee=mentee, mentor=mentor, status='completed')
            if not completed_bookings.exists():
                raise ValidationError("You have no completed bookings with this mentor for feedback.")

            # Save feedback with the specified mentor
            serializer.save(mentee=mentee, mentor=mentor)

        except Mentee.DoesNotExist:
            raise ValidationError("You do not have an associated Mentee profile.")
        
        
        # try:
        #     if hasattr(self.request.user, 'mentee'):
        #         mentee = self.request.user.mentee_profile
        #         serializer.save(mentee=mentee)
        #     else:
        #         raise ValueError("User does not have an associated Mentee.")
        # except AttributeError:
        #     # Handle the case where the user is not a mentee
        #     raise ValueError("User does not have an associated Mentee.")
        






# Email Verification View

from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailVerificationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            user.is_verified = True  # Mark as verified
            user.is_active = True  # Activate the account
            user.verification_token = None  # Clear the token
            user.save()

            # Create profile based on user type
            if user.user_type == 'mentor':
                Mentor.objects.create(user=user)  # Create the mentor instance
            elif user.user_type == 'mentee':
                Mentee.objects.create(user=user)  # Create the mentee instance


            return Response({"message": "Email verified successfully!"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "Invalid token."}, status=400)

class MentorSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = MentorSignupSerializer  # Serializer to handle user creation
    permission_classes = [permissions.AllowAny]

class MenteeSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = MenteeSignupSerializer  # Serializer to handle user creation
    permission_classes = [permissions.AllowAny]


from agora_token_builder import RtcTokenBuilder
from django.conf import settings
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from django.utils import timezone
from .models import Mentor, Mentee, Booking
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.urls import reverse

class TokenGenerationView(generics.GenericAPIView):

    # permission_classes = [IsAuthenticated]  # Only allow authenticated users

    def get(self, request):
        channel_name = request.query_params.get('channel')
        uid = request.user.id
        
        if not channel_name:
            return Response({"error": "Channel name is required"}, status=400)

        AGORA_APP_ID = settings.AGORA_APP_ID
        AGORA_APP_CERTIFICATE = settings.AGORA_APP_CERTIFICATE

        token = RtcTokenBuilder.buildTokenWithUid(
            AGORA_APP_ID,
            AGORA_APP_CERTIFICATE,
            channel_name,
            uid,
            1,  # Use 1 for Attendee role
            3600  # Token expiration time in seconds
        )

        return Response({"token": token})

class CallViewSet(viewsets.ViewSet):

    # permission_classes = [IsAuthenticated]  # Only allow authenticated users

    def generate_user_token(self, channel_name, user_id):
        return RtcTokenBuilder.buildTokenWithUid(
            settings.AGORA_APP_ID,
            settings.AGORA_APP_CERTIFICATE,
            channel_name,
            user_id,
            1,  # Use Attendee role
            3600
        )

    def request_call(self, request, mentor_id):
        user = request.user

        mentee = None  # Initialize mentee
        mentor = None  # Initialize mentor

        if hasattr(user, 'mentee_profile'):
            mentee = user.mentee_profile
            role = 'mentee'
        elif hasattr(user, 'mentor_profile'):
            mentor = user.mentor_profile
            role = 'mentor'
        else:
            raise PermissionDenied("User must be either a mentee or a mentor.")

        try:
            mentor = Mentor.objects.get(id=mentor_id)

        except Mentor.DoesNotExist:
            return Response({"error": "Mentor not found."}, status=404)


        # Get the current time and define the end time
        current_time = timezone.now()
        end_time = current_time + timezone.timedelta(minutes=150)

        
        # Query for upcoming confirmed bookings within the next 150 minutes for the specified mentor
        try:
            booking = Booking.objects.get(
                mentor=mentor,
                status='confirmed',
                scheduled_time__range=(current_time, end_time)
            )
            mentee = booking.mentee  # Get the mentee associated with the booking
        except Booking.DoesNotExist:
            return Response({"error": "No confirmed bookings within the next 150 minutes."}, status=404)


        current_time = timezone.now()
        time_difference = (booking.scheduled_time - current_time).total_seconds() / 60  # Difference in minutes

        if time_difference > 1500:
            return Response({"error": "Call can only be initiated 1500 minutes before the scheduled time."}, status=403)

        channel_name = f"call-{mentor.id}-{mentee.id}-{booking.id}"


        # Generate token for the caller
        user_token = self.generate_user_token(channel_name, mentee.user.id if role == 'mentee' else mentor.user.id)


        # # Create the meeting link
        # meeting_link = f"{request.build_absolute_uri(reverse('your_meeting_view_name'))}?channel={channel_name}&token={user_token}"
    
        # # Send email to mentor and mentee
        # subject = "Your Scheduled Call Link"
        # message = f"Hi,\n\nYou have a scheduled call. Click the link below to join:\n{meeting_link}\n\nThanks!"
        
        # send_mail(subject, message, settings.EMAIL_HOST_USER, [mentor.user.email, mentee.user.email])

        return Response({
            "mentor_id": mentor.id,
            "mentee_id": mentee.id,
            "channel_name": channel_name,
            "user_token": user_token,
            # "meeting_link": meeting_link
        })
    

    def accept_call(self, request, channel_name):
        user = request.user

        if hasattr(user, 'mentee_profile'):
            mentee = user.mentee_profile
            role = 'mentee'
        elif hasattr(user, 'mentor_profile'):
            mentor = user.mentor_profile
            role = 'mentor'
        else:
            raise PermissionDenied("User must be either a mentee or a mentor.")

        # Check if the call can be accepted based on the existing bookings
        try:
            booking = Booking.objects.get(channel_name=channel_name)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=404)

        # Generate token for the caller
        user_token = self.generate_user_token(channel_name, mentee.user.id if role == 'mentee' else mentor.user.id)

        # # Create the meeting link
        # meeting_link = f"{request.build_absolute_uri(reverse('your_meeting_view_name'))}?channel={channel_name}&token={user_token}"

        # # Send email to mentor and mentee
        # subject = "Your Scheduled Call Link"
        # message = f"Hi,\n\nYou have a scheduled call. Click the link below to join:\n{meeting_link}\n\nThanks!"
        
        # send_mail(subject, message, settings.EMAIL_HOST_USER, [mentor.user.email, mentee.user.email])

        return Response({
            "mentor_id": mentor.id,
            "mentee_id": mentee.id,
            "channel_name": channel_name,
            "user_token": user_token,
            # "meeting_link": meeting_link
        })


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        # Optionally, you can add logic here before saving, such as assigning a creator
        serializer.save()

class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

# chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Group, GroupMessage
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Group, Membership
from .serializers import GroupListSerializer, GroupSerializer, MemberDetailSerializer
from rest_framework import viewsets
from users.models import OTP


class GroupChatView(LoginRequiredMixin, View):
    login_url = '/api/users/login/'  # Redirect to this URL if not logged in
    redirect_field_name = 'next'  # Redirect to the original URL after login

    def get(self, request, group_id="1"):
        print(f"Request user: {request.user}")
        print(f"User is authenticated: {request.user.is_authenticated}")
        print(f"Session data: {request.session.items()}") 

        group = get_object_or_404(Group, id=group_id)
        messages = GroupMessage.objects.filter(group=group).order_by('timestamp')
        print("I'm here in GroupChatView")

        # return redirect(f'/chat/{group_id}/')
        return render(request, 'chat/group_chat.html', {'group': group, 'messages': messages})


class JoinGroupView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        user = request.user

        # Check if the user is already a member
        if not Membership.objects.filter(user=user, group=group).exists():
            # Create a membership
            Membership.objects.create(user=user, group=group, user_type=user.user_type)

        return Response({"message": "Joined the group successfully."}, status=200)
    

# class GroupListViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Group.objects.prefetch_related('membership_set__user')  # Pre-fetch memberships and associated users
    
#     # Use different serializers for listing and detail views
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
       
#             return GroupSerializer  # Use GroupSerializer for detail view
#         return GroupListSerializer  # Use GroupListSerializer for list view

#     def retrieve(self, request, *args, **kwargs):
#         # Retrieve the specific group
#         return super().retrieve(request, *args, **kwargs)


class GroupListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.prefetch_related('membership_set__user')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GroupSerializer  # Detailed view
        return GroupListSerializer  # Listing view

    def get_permissions(self):
        if self.action == 'retrieve':
            self.authentication_classes = [TokenAuthentication]
            return [IsAuthenticated()]
        return []  # Allow public access for listing


class GroupMembersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberDetailSerializer

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        return Membership.objects.filter(group_id=group_id).select_related('user')


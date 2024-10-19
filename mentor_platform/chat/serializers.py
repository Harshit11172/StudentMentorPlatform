from rest_framework import serializers
from .models import Group, GroupMessage, Membership
from django.contrib.auth import get_user_model

User = get_user_model() 

class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'college', 'country', 'url', 'member_count', 'mentor_count', 'mentee_count']


class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = ['id', 'group', 'sender', 'content', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# class MembershipSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)  
#     user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)

#     class Meta:
#         model = Membership
#         fields = ['user', 'user_id', 'user_type', 'username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active', 'user_permissions']


class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)  # From User model
    email = serializers.EmailField(source='user.email', read_only=True)        # From User model
    first_name = serializers.CharField(source='user.first_name', read_only=True)  # From User model
    last_name = serializers.CharField(source='user.last_name', read_only=True)    # From User model
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)  # From User model
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)  # From User model
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)      # From User model
    user_permissions = serializers.PrimaryKeyRelatedField(source='user.user_permissions', read_only=True, many=True)  # From User model

    class Meta:
        model = Membership
        fields = ['user', 'user_id', 'username', 'user_type', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active', 'user_permissions']


class GroupSerializer(serializers.ModelSerializer):
    admins = UserSerializer(many=True)
    members = MembershipSerializer(many=True, required=False, source='membership_set')

    class Meta:
        model = Group
        fields = [
            'id', 'group_name', 'admins', 'members', 
            'college', 'country', 'url', 
            'member_count', 'mentor_count', 'mentee_count'
        ]


class MemberDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Assuming you already have UserSerializer defined

    class Meta:
        model = Membership
        fields = ['user', 'user_type']

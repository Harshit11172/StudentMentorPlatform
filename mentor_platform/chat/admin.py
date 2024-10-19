from django.contrib import admin
from .models import Group, Membership, GroupMessage

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1  # Number of empty forms to display

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name', 'get_admins', 'member_count', 'mentor_count', 'mentee_count')
    search_fields = ('group_name', 'college', 'country')
    inlines = [MembershipInline]  # Display memberships inline

    def get_admins(self, obj):
        return ", ".join([admin.username for admin in obj.admins.all()])
    get_admins.short_description = 'Admins'  # Column header in admin

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('members', 'admins')  # Optimize query

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('user__username', 'group__group_name')

class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'content', 'timestamp')
    list_filter = ('group', 'sender')
    search_fields = ('content',)

# Registering the models with the admin site
admin.site.register(Group, GroupAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)

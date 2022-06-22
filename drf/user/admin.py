from django.contrib import admin
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User, UserProfile, Hobby

# 사용 방법은 TabulaInline과 StackedInline 모두 동일
# 둘 다 사용해보고 뭐가 좋은지 비교해보기
# class UserProfileInline(admin.TabularInline):

# StackedInline 세로 TabularInline 가로


class UserProfileInline(admin.StackedInline):
    model = UserProfileModel
    filter_horizontal = ['hobby']


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'fullname')
#     inlines = (UserProfileInline,)

class UserAdmin(BaseUserAdmin):

    list_display = ('id', 'username', 'fullname', 'email')
    list_display_links = ('username',)
    list_filter = ('username',)
    search_fields = ('username', 'email',)

    fieldsets = (
        ("info", {'fields': ('username', 'password',
         'email', 'fullname', 'join_date',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)}),
    )
    inlines = (
        UserProfileInline,
    )

    add_fieldsets = (
        ( None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password1', 'password2')}),)

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date')
        else:
            return('join_date',)


# Register your models here.
admin.site.register(UserModel, UserAdmin)
# admin.site.register(User,UserAdmin)  # admin.site.register(User,UserAdmin)
admin.site.register(UserProfileModel)
admin.site.register(HobbyModel)

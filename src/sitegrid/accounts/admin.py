from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth import get_user_model

User = get_user_model()


ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('prefix', 'middle_name', 'suffix', 'contact_phone', 'contact_email', )}),
)

class UserAdmin(BaseUserAdmin):
  
  
    def full_name(self, obj):
        return obj.get_full_name
        

    list_display = ('username', 'full_name', 'email', 'contact_email', 'last_login')
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = BaseUserAdmin.fieldsets + ADDITIONAL_USER_FIELDS

    save_on_top = True

# Re-register UserAdmin
#admin.site.unregister(User)
admin.site.register(User, UserAdmin)


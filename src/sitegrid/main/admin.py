from django.contrib import admin

from main.models import GeneralSetting, PhoneNumber




class GeneralSettingAdmin(admin.ModelAdmin):
    
    list_display = ('key', 'last_modified', )

    save_on_top = True
    


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('e164_number', 'ext', 'number_type', )


    save_on_top = True


admin.site.register(GeneralSetting, GeneralSettingAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)



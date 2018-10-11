from django.contrib import admin

from clients.models import ClientAccount, ClientContact, ClientConnection


class ContactAccountInline(admin.TabularInline):
    model = ClientConnection
    extra = 1


class ClientAccountAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'city', 'state', 'country', )

    save_on_top = True
    
    inlines = [
        ContactAccountInline,
        ]

class ClientContactAdmin(admin.ModelAdmin):
    list_display = ('user', )

    
    raw_id_fields = ('user', )
    save_on_top = True

    inlines = [
        ContactAccountInline,
        ]


admin.site.register(ClientAccount, ClientAccountAdmin)
admin.site.register(ClientContact, ClientContactAdmin)
from django.contrib import admin

from logs.models import Error, MasterLog


class ErrorAdmin(admin.ModelAdmin):
  
    list_display = ('error_class', 'message', 'thrown_on', 'location', 'server',)
    ordering = ('-thrown_on',)
    search_fields = ('error_class', 'message', 'error_trace',)
    

class MasterLogAdmin(admin.ModelAdmin):
  
    list_display = ('entry_type', 'message', 'location', 'date_created',)
    ordering = ('-date_created',)
    search_fields = ('entry_type', 'message', )    
    
admin.site.register(Error, ErrorAdmin)    
admin.site.register(MasterLog, MasterLogAdmin)    


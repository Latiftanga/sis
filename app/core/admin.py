from django.contrib import admin
from core.models import SignupToken, User
from core.utils import generate_unique_token

class SignupTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'is_used', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('token', 'created_at')
    actions = ['generate_token']

    def generate_token(self, request, queryset):
        for obj in queryset:
            if not obj.token:
                obj.token = generate_unique_token()
                obj.save()
        self.message_user(request, "Tokens generated successfully.")
    
    generate_token.short_description = "Generate Token for Selected Users"

admin.site.register(SignupToken, SignupTokenAdmin)
admin.site.register(User)
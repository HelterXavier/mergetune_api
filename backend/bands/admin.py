from django.contrib import admin
from .models import Band, BandMembership
from api.admin_utils import NoBulkActionsMixin


class BandMembershipInline(admin.TabularInline):
    model = BandMembership
    extra = 0
    fields = ('user', 'role', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['user']

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Band)
class BandAdmin(NoBulkActionsMixin, admin.ModelAdmin):
    list_display = ('name', 'created_by')
    inlines = [BandMembershipInline]
    exclude = ('created_by', 'created_at', 'updated_at')
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(BandMembership)
class BandMembershipAdmin(NoBulkActionsMixin, admin.ModelAdmin):
    list_display = ('user', 'band', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__name', 'user__email', 'band__name')
    readonly_fields = ('created_at',)
    autocomplete_fields = ['user', 'band']

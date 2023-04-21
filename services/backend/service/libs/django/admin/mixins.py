from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin


class BaseReadOnlyAdminMixin(BaseModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyModelAdminMixin(BaseReadOnlyAdminMixin):
    def has_add_permission(self, request):
        return False


class ReadOnlyInlineMixin(BaseReadOnlyAdminMixin, InlineModelAdmin):
    def has_add_permission(self, request, obj):
        return False

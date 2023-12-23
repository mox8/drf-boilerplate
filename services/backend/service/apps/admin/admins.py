from django.contrib.auth import get_user_model

from apps.admin.site import admin_site


admin_site.register(get_user_model())

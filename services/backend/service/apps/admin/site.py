from django.conf import settings
from django.contrib.admin import AdminSite


class LandingAdminSite(AdminSite):
    site_header = f'{settings.PROJECT_NAME} Admin'
    site_title = f'{settings.PROJECT_NAME} Portal'
    index_title = f'Welcome to {settings.PROJECT_NAME} admin panel '


admin_site = LandingAdminSite(name='admin_site')

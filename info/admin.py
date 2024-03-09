from django.contrib import admin

from . import models

class OrganisationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("organisation_name",)}

admin.site.register(models.Region)
admin.site.register(models.Location)
admin.site.register(models.Organisation, OrganisationAdmin)
admin.site.register(models.Resource)
admin.site.register(models.Event)
admin.site.register(models.Contact)
admin.site.register(models.Scheduler)

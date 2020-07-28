from django.contrib import admin
from .models import Sku, Subgroup, Warehouse, Proposal, Mo, WorkCenter, Schedule, Constraint, FabricShortage

# Register your models here.
admin.site.register(Sku)
admin.site.register(Subgroup)
admin.site.register(Warehouse)
admin.site.register(Proposal)
admin.site.register(Mo)
admin.site.register(WorkCenter)
admin.site.register(Schedule)
admin.site.register(Constraint)
admin.site.register(FabricShortage)

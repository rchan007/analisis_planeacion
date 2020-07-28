#resources.py  
from django.db import IntegrityError
from import_export.fields import Field
from import_export import resources, widgets  
from .models import Sku, Warehouse, Subgroup, Proposal, WorkCenter, Mo, Schedule, Constraint

class SkuResource(resources.ModelResource):
  name = Field(attribute='name', column_name='sku')
  
  class Meta:
    model = Sku
    skip_unchanged = True
    report_skipped = True
    exclude = ('name',)
  
  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass

class WarehouseResource(resources.ModelResource):
  name = Field(attribute='name', column_name='warehouse')
  
  class Meta:
    model = Warehouse
    skip_unchanged = True
    report_skipped = True
    exclude = ('name',)
  
  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass

class SubgroupResource(resources.ModelResource):
  name = Field(attribute='name', column_name='subgroup')
  class Meta:
    model = Subgroup
    skip_unchanged = True
    report_skipped = True
    exclude = ('name',)
  
  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass

class ProposalResource(resources.ModelResource):
  name = Field(attribute='name', column_name='name')
  planner = Field(attribute='planner', column_name='planner')
  spreading = Field(attribute='spreading', column_name='spreading')
  position = Field(attribute='position', column_name='position')
  grand_total = Field(attribute='grand_total', column_name='grand_total')
  sku_id = Field(attribute='sku_id', column_name='sku', widget=widgets.ForeignKeyWidget(Sku, 'name'))
  warehouse_id = Field(attribute='warehouse_id', column_name='warehouse', widget=widgets.ForeignKeyWidget(Warehouse, 'name'))
  subgroup_id = Field(attribute='subgroup_id', column_name='subgroup', widget=widgets.ForeignKeyWidget(Subgroup, 'name'))
  workcenter_id = Field(attribute='workcenter_id', column_name='workcenter', widget=widgets.ForeignKeyWidget(WorkCenter, 'name'))
  class Meta:
    model = Proposal
    skip_unchanged = True
    report_skipped = True
  
  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass

class WorkcenterProposalResource(resources.ModelResource):
  name = Field(attribute='name', column_name='workcenter')
  warehouse_id = Field(attribute='warehouse_id', column_name='warehouse', widget=widgets.ForeignKeyWidget(Warehouse, 'name'))
  subgroup_id = Field(attribute='subgroup_id', column_name='subgroup', widget=widgets.ForeignKeyWidget(Subgroup, 'name'))

  class Meta:
    model = WorkCenter
    skip_unchanged = True
    report_skipped = True
  
  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass

class WorkcenterResource(resources.ModelResource):
  name = Field(attribute='name', column_name='workcenter')
  line = Field(attribute='line', column_name='line')
  warehouse_id = Field(attribute='warehouse_id', column_name='warehouse', widget=widgets.ForeignKeyWidget(Warehouse, 'name'))
  subgroup_id = Field(attribute='subgroup_id', column_name='subgroup', widget=widgets.ForeignKeyWidget(Subgroup, 'name'))

  class Meta:
    model = WorkCenter
    skip_unchanged = True
    report_skipped = True
    exclude = ('status',)
  
  def save_instance(self, instance, using_transactions=True, dry_run=True):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass


class WorkcenterConstraintResource(resources.ModelResource):
  name = Field(attribute='name', column_name='workcenter')
  line = Field(attribute='line', column_name='line')
  warehouse_id = Field(attribute='warehouse_id', column_name='warehouse', widget=widgets.ForeignKeyWidget(Warehouse, 'name'))

  class Meta:
    model = WorkCenter
    skip_unchanged = True
    report_skipped = True
  
  def after_export(self, queryset, data, *args, **kwargs):
        queryset.update(exported=True)
  
  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass

class ScheduleResource(resources.ModelResource):
  number = Field(attribute='number', column_name='schedule')

  class Meta:
    model = Schedule
    skip_unchanged = True
    report_skipped = True
  
  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass

class MoResource(resources.ModelResource):
  number = Field(attribute='number', column_name='mo')
  status = Field(attribute='status', column_name='status_mo')
  schedule_id = Field(attribute='schedule_id', column_name='schedule', widget=widgets.ForeignKeyWidget(Schedule, 'number'))
  sku_id = Field(attribute='sku_id', column_name='sku', widget=widgets.ForeignKeyWidget(Sku, 'name'))
  workcenter_id = Field(attribute='workcenter_id', column_name="workcenter", widget=widgets.ForeignKeyWidget(WorkCenter, 'name'))
  entry_date = Field(attribute='entry_date', column_name='entry_date', widget=widgets.DateWidget())
  finish_date = Field(attribute='finish_date', column_name='finish_date', widget=widgets.DateWidget())
  order_qty = Field(attribute='order_qty', column_name='order_qty')
  received_qty = Field(attribute='received_qty', column_name='received_qty')
  project = Field(attribute='project', column_name='project')
  
  class Meta:
    model = Mo
    skip_unchanged = True
    report_skipped = True
  
  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass
  
class ConstraintResource(resources.ModelResource):
  period = Field(attribute='period', column_name='period')
  line = Field(attribute='line', column_name='line')
  status = Field(attribute='status', column_name='status')
  comments = Field(attribute='comments', column_name='comments')
  sah_avg = Field(attribute='sah_avg', column_name='sah_avg')
  sah_goal = Field(attribute='sah_goal', column_name='sah_goal')
  workcenter_id = Field(attribute='workcenter_id', column_name='workcenter', widget=widgets.ForeignKeyWidget(WorkCenter, 'name'))
  
  class Meta:
    model = Constraint
    skip_unchanged = True
    report_skipped = True

  def save_instance(self, instance, using_transactions=True, dry_run=False):
    try:
      super().save_instance(instance, using_transactions, dry_run)
    except IntegrityError:
      pass
from django.db import models
import math

class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)
    create_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Subgroup(models.Model):
    name = models.CharField(max_length=30, unique=True)
    create_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Sku(models.Model):
    name = models.CharField(max_length=50, unique=True)
    create_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WorkCenter(models.Model):
    name = models.CharField(max_length=30, unique=True)
    line = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    create_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Proposal(models.Model):
    name = models.CharField(max_length=30)
    planner = models.CharField(max_length=50)
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    subgroup_id = models.ForeignKey(Subgroup, on_delete=models.CASCADE)
    workcenter_id = models.ForeignKey(WorkCenter, on_delete=models.CASCADE, null=True, blank=True)
    sku_id = models.ForeignKey(Sku, on_delete=models.CASCADE)
    spreading = models.CharField(max_length=50)
    position = models.FloatField()
    grand_total = models.IntegerField()
    create_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'planner', 'warehouse_id', 'subgroup_id', 'sku_id')

    def __str__(self):
        return self.name

class Schedule(models.Model):
    number = models.CharField(max_length=30, unique=True)
    mrr_date = models.DateField(null=True)
    optiplan_date = models.DateField(null=True)
    eliminate_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    create_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number

class FiscalCalendar(models.Model):
    date = models.DateField()
    month_name = models.CharField(max_length=30)
    day_name = models.CharField(max_length=50)
    month_number = models.IntegerField()
    week_number = models.IntegerField()
    year_number = models.IntegerField()

class Mo(models.Model):
    number = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=10)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    sku_id = models.ForeignKey(Sku, on_delete=models.CASCADE)
    workcenter_id = models.ForeignKey(WorkCenter, on_delete=models.CASCADE, null=False)
    entry_date = models.DateField()
    finish_date = models.DateField()
    order_qty = models.IntegerField()
    received_qty = models.IntegerField()
    project = models.CharField(max_length=50, null=True, blank=True)
    fiscal_date = models.ForeignKey(FiscalCalendar, null=True, on_delete=models.SET_NULL)

    @property
    def balance(self):
        try:
            return math.ceil((self.order_qty - self.received_qty))
        except:
            return 0

    def __str__(self):
        return self.number

class Constraint(models.Model):
    period = models.CharField(max_length=30)
    status = models.CharField(max_length=50)
    sah_avg = models.FloatField()
    sah_goal = models.FloatField()
    comments = models.CharField(max_length=50, blank=True)
    workcenter_id = models.ForeignKey(WorkCenter, on_delete=models.CASCADE)
    create_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('period', 'status', 'workcenter_id')

    @property
    def pieces_goal(self):
        try:
            return math.ceil((self.sah_goal / self.sah_avg))
        except:
            return 0
    
    def __str__(self):
        return self.period

class FabricShortage(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE)
    workcenter = models.ForeignKey(WorkCenter, on_delete=models.CASCADE)
    pcs_to_issue = models.IntegerField(null=False)
    pcs_short = models.IntegerField(null=False)
    no_fabric = models.CharField(max_length=50, null=False)
    comments = models.TextField(null=True, blank=True)
    create_att = models.DateTimeField(auto_now_add=True)
    updated_att = models.DateTimeField(auto_now_add=True)



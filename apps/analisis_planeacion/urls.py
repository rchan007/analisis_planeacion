from django.urls import path, include
from .views import importar_proposal, importar_mmz733, importar_constraint, constraintList, constraintListFiltered, \
ConstraintNew, ConstraintUpdate, ConstraintDelete, PlanningLogList, \
AnalisisPlaneacionList, WorkCenterList, DetallesScheduleList, PlanningLogUpdateMrr,\
PlanningLogUpdateOptiplan, ConfirmDeleteSchedule, DeleteSchedule, PlanningLogUpdate, \
PlanningLogListDeteleted, ReturnScheduleDeleted, FabricShortageNew, FabricShortageList, FabricShortageUpdate, FabricShortageDelete, \
import_fiscal_calendar, FabricShortageReport, planning_log_resume

urlpatterns = [
    path('import/proposal', importar_proposal, name="import_proposal"),
    path('import_mmz733/', importar_mmz733, name="import_mmz733"),
    path('import/constraint', importar_constraint, name="import_constraint"),
    path('import/fiscal_calendar', import_fiscal_calendar, name="import_fiscal_calendar"),
    path('constraint/list', constraintList, name="constraint_list"),
    path('constraint/list/<constraint_period>', constraintListFiltered, name="constraint_list_filtered"),
    path('constraint/new', ConstraintNew.as_view(), name="constraint_new"),
    path('constraint/edit/<pk>', ConstraintUpdate.as_view(), name='constraint_edit'),
    path('constraint/delete/<pk>', ConstraintDelete.as_view(), name='constraint_delete'),
    path('planning_log/list', PlanningLogList, name='planning_log_list'),
    path('planning_log/resume', planning_log_resume, name='planning_log_resume'),
    path('planning_log/schedules_eliminados', PlanningLogListDeteleted, name='planning_log_list_deleted'),
    path('planning_log/detalles_schedule/<schedule_id>', DetallesScheduleList, name='detalle_schedule_list'),
    path('planning_log/update_mrr_date/<schedule_id>', PlanningLogUpdateMrr, name="update_mrr_date"),
    path('planning_log/update_optiplan_date/<schedule_id>', PlanningLogUpdateOptiplan, name="update_optiplan_date"),
    path('planning_log/confirm_delete/<schedule_id>', ConfirmDeleteSchedule, name='confirm_schedule_delete'),
    path('planning_log/delete/<schedule_id>', DeleteSchedule, name='schedule_delete'),
    path('planning_log/return_schedule_deleted/<schedule_id>', ReturnScheduleDeleted, name='return_schedule_deleted'),
    path('planning_log/upate_comments/<pk>', PlanningLogUpdate.as_view(), name='update_planning_log_comments'),
    path('analisis_planeacion/list', AnalisisPlaneacionList, name='analisis_planeacion_list'),
    path('workcenter/list', WorkCenterList, name='work_center_list'),
    path('fabric_shortage/list', FabricShortageList, name='fabric_shortage_list'),
    path('fabric_shortage/new', FabricShortageNew.as_view(), name='fabric_shortage_new'),
    path('fabric_shortage/update/<pk>', FabricShortageUpdate.as_view(), name='fabric_shortage_update'),
    path('fabric_shortage/delete/<pk>', FabricShortageDelete.as_view(), name='fabric_shortage_delete'),
    path('fabric_shortage/report', FabricShortageReport, name='fabric_shortage_report'),
]

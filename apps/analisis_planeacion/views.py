import io
import csv
from tablib import Dataset
from itertools import chain
from django.utils import timezone
from datetime import datetime
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, Value, Count, F, Q, CharField
from django.db.models.functions import Concat
from .forms import FormConstraint, FormSchedule, FormFabricShortage
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Constraint, Schedule, Mo, Proposal, WorkCenter, Warehouse,Subgroup, \
                    Sku, FabricShortage, FiscalCalendar

def convert_date(date):
    '''Convert a date to a new date available for the database'''
    result = date.split('/')
    date_stamp = datetime(int(result[2]), int(result[0]), int(result[1]))
    return date_stamp.strftime('%Y-%m-%d')

def get_csv_file(request):
    '''Return a csv file available for the server'''
    report = request.FILES['csvfile']
    dataset = report.read().decode('utf-8')
    io_string = io.StringIO(dataset)
    next(io_string) #Jump to the next file or Jump the titles
    return io_string

def import_fiscal_calendar(request):
    '''Import the data of the csv file fiscal_calendar to the database'''
    if request.method == 'POST':
        for column in csv.reader(get_csv_file(request), delimiter=','):
            fiscal_calendar_item = FiscalCalendar.objects.filter(date=convert_date(column[0]))
            if not fiscal_calendar_item:
                FiscalCalendar.objects.create(
                    date = convert_date(column[0]),
                    month_name = column[1],
                    day_name = column[4],
                    month_number = column[2],
                    week_number = column[3],
                    year_number = column[5],
                )
        for mo in Mo.objects.all():
            for f_date in FiscalCalendar.objects.all():
                if mo.fiscal_date == f_date.date:
                    mo.fiscal_date = f_date.date
                    mo.save()

    return render(request, 'export/import.html')


def importar_proposal(request):
    if request.method == 'POST':
        
        for column in csv.reader(get_csv_file(request), delimiter=','):
            sku = Sku.objects.filter(name=column[5])
            if not sku:
                Sku.objects.create(
                    name = column[5]
                )
            warehouse = Warehouse.objects.filter(name=column[3])
            if not warehouse:
                Warehouse.objects.create(
                    name = column[3]
                )
            subgroup = Subgroup.objects.filter(name=column[4])
            if not subgroup:
                Subgroup.objects.create(
                    name = column[4]
                )
            if column[2] == '':
                pass
            else:
                workcenter = WorkCenter.objects.filter(name=column[2])
                if not workcenter:
                    WorkCenter.objects.create(
                        name = column[2],
                        warehouse_id = Warehouse.objects.get(name=column[3])
                    )
            proposal = Proposal.objects.filter(name=column[0], planner=column[1], 
                                                warehouse_id=Warehouse.objects.get(name=column[3]),
                                                subgroup_id=Subgroup.objects.get(name=column[4]),
                                                sku_id=Sku.objects.get(name=column[5]))
            if not proposal:
                if column[2] == '':
                    Proposal.objects.create(
                        name = column[0],
                        planner = column[1],
                        warehouse_id = Warehouse.objects.get(name=column[3]),
                        subgroup_id = Subgroup.objects.get(name=column[4]),
                        sku_id = Sku.objects.get(name=column[5]),
                        spreading = column[6],
                        position = column[7],
                        grand_total = column[8],
                    )
                else:  
                    Proposal.objects.create(
                        name = column[0],
                        planner = column[1],
                        warehouse_id = Warehouse.objects.get(name=column[3]),
                        subgroup_id = Subgroup.objects.get(name=column[4]),
                        sku_id = Sku.objects.get(name=column[5]),
                        workcenter_id = WorkCenter.objects.get(name=column[2]),
                        spreading = column[6],
                        position = column[7],
                        grand_total = column[8],

                    )    
    
    return render(request, 'export/import.html')

def importar_mmz733(request):
    if request.method == 'POST':
        for column in csv.reader(get_csv_file(request), delimiter=','):
            sku =  Sku.objects.filter(name=column[4])
            if not sku:
                Sku.objects.create(name=column[4])
            
            warehouse = Warehouse.objects.filter(name=column[0])
            if not warehouse:
                Warehouse.objects.create(name=column[0])
            
            workcenter = WorkCenter.objects.filter(name=column[1])
            if not workcenter:
                WorkCenter.objects.create(
                    name = column[1],
                    warehouse_id = Warehouse.objects.get(name=column[0]),
                )
            
            if column[6] == '':
                pass
            else:
                schedule = Schedule.objects.filter(number=column[6])
                if not schedule:
                    Schedule.objects.create(number = column[6],)       
            
            mo = Mo.objects.filter(number=column[5])
            entry_date = convert_date(column[2])
            finish_date = convert_date(column[3])
            if not mo:
                Mo.objects.create(
                    number = column[5],
                    status = column[7],
                    schedule_id = Schedule.objects.get(number=column[6]),
                    sku_id = Sku.objects.get(name=column[4]),
                    workcenter_id = WorkCenter.objects.get(name=column[1]),
                    entry_date = entry_date,
                    finish_date = finish_date,
                    order_qty = column[8],
                    received_qty = column[9],
                    project = column[10],
                    fiscal_date = FiscalCalendar.objects.get(date=entry_date),
                )
            else:
                Mo.objects.filter(number=column[5]).update(status=column[7])
                Mo.objects.filter(number=column[5]).update(order_qty=column[8])
                Mo.objects.filter(number=column[5]).update(received_qty=column[9])
                Mo.objects.filter(number=column[5]).update(entry_date=entry_date)
                Mo.objects.filter(number=column[5]).update(finish_date=finish_date)
                Mo.objects.filter(number=column[5]).update(fiscal_date=FiscalCalendar.objects.get(date=entry_date))
                Mo.objects.filter(number=column[5]).update(project=column[10])
    return render(request, 'export/import.html')

def importar_constraint(request):
    if request.method == 'POST':
        report = request.FILES['csvfile']
        dataset = report.read().decode('utf-8')
        io_string = io.StringIO(dataset)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            warehouse = Warehouse.objects.filter(name=column[1])
            if not warehouse:
                Warehouse.objects.create(
                    name = column[1]
                )
            workcenter = WorkCenter.objects.filter(name=column[2])
            if not workcenter:
                created = WorkCenter.objects.create(
                    name = column[2],
                    line = column[3],
                    status = 'New',
                    warehouse_id = Warehouse.objects.get(name=column[1]),
                )
            else:
                WorkCenter.objects.filter(name=column[2]).update(line=column[3])
                WorkCenter.objects.filter(name=column[2]).update(status='Normal')
            
            try:
                created = Constraint.objects.update_or_create(
                    period = column[0],
                    status = column[4],
                    sah_avg = column[5],
                    sah_goal = column[6],
                    workcenter_id = WorkCenter.objects.get(name=column[2]),
                )
            except:
                updated_sah_avg = Constraint.objects.filter(period=column[0]).\
                                                    filter(status=column[4]).\
                                                    filter(workcenter_id=WorkCenter.objects.get(name=column[2])).\
                                                    update(sah_avg=column[5])
                updated_sah_goal = Constraint.objects.filter(period=column[0]).\
                                                    filter(status=column[4]).\
                                                    filter(workcenter_id=WorkCenter.objects.get(name=column[2])).\
                                                    update(sah_goal=column[6])
        io_string = io.StringIO(dataset)
        next(io_string)
        workcenters = WorkCenter.objects.all()
        for workcenter in workcenters:
            #start with the status No encontrado
            status = 'No encontrado'
            for column in csv.reader(io_string, delimiter=','):
                data = WorkCenter.objects.filter(name=column[2])
                if data:
                    #if it is founded we change the status
                    status = 'Encontrado'
                    break
            if status == 'No encontrado':
                #only change the 
                WorkCenter.objects.filter(name=workcenter.name).update(status='Drop')

        
    return render(request, 'export/import.html')

def constraintList(request):
    last_constraint = Constraint.objects.order_by('-id')[0]
    if request.method == 'GET':
        constraint_names = Constraint.objects.values('period').\
                                            order_by('-create_att__month','-create_att__day').\
                                            distinct()
       
        constraint  = Constraint.objects.all().filter(period=last_constraint.period)
        
        return render(request, 'constraint/list.html', {
            'constraint': constraint,
            'constraint_names': constraint_names,
        })

def constraintListFiltered(request, constraint_period):
        if request.method == 'GET':
            constraint_names = Constraint.objects.values('period').\
                                                    order_by('-create_att__month', 
                                                            '-create_att__day').\
                                                    distinct()
            constraint  = Constraint.objects.all().filter(period=constraint_period)
            
            return render(request, 'constraint/list_filtered.html', {
                'constraint_period': constraint_period,
                'constraint': constraint,
                'constraint_names': constraint_names,
            })

class ConstraintNew(CreateView):
    model = Constraint
    form_class = FormConstraint
    template_name = 'constraint/new.html'
    success_url = 'fabric_shortage_list'

class FabricShortageNew(CreateView):
    model: FabricShortage
    form_class = FormFabricShortage
    template_name = 'shortage/new.html'
    success_url = reverse_lazy('fabric_shortage_list')

def FabricShortageList(request):
    fabric_shortage = FabricShortage.objects.filter(create_att__day=timezone.localtime(timezone.now()).day)
    return render(request, 'shortage/list.html', {
        'fabric_shortage': fabric_shortage,
    })

class ConstraintUpdate(UpdateView):
    model = Constraint
    form_class = FormConstraint
    template_name = 'constraint/new.html'
    success_url = reverse_lazy('constraint_list')


class FabricShortageUpdate(UpdateView):
    model = FabricShortage
    form_class = FormFabricShortage
    template_name = 'shortage/new.html'
    success_url = reverse_lazy('fabric_shortage_list')

class FabricShortageDelete(DeleteView):
    model =  FabricShortage
    template_name = 'shortage/delete.html'
    success_url = reverse_lazy('fabric_shortage_list')

class PlanningLogUpdate(UpdateView):
    model = Schedule
    form_class = FormSchedule
    template_name = 'planning_log/update.html'
    success_url = reverse_lazy('planning_log_list')


class ConstraintDelete(DeleteView):
    model = Constraint
    template_name = 'constraint/delete.html'
    success_url = reverse_lazy('constraint_list')

def PlanningLogList(request):
    schedules = Schedule.objects.raw("SELECT `analisis_planeacion_schedule`.`id`, \
    `analisis_planeacion_schedule`.`number`, `analisis_planeacion_schedule`.`comments`, \
    `analisis_planeacion_schedule`.`mrr_date`, `analisis_planeacion_schedule`.`optiplan_date`,\
    `analisis_planeacion_mo`.`finish_date`, `analisis_planeacion_workcenter`.`name`, \
    `analisis_planeacion_mo`.`project`, SUM(`analisis_planeacion_mo`.`order_qty`) AS \
    `total_schedule` FROM `analisis_planeacion_schedule` INNER JOIN \
    `analisis_planeacion_mo` ON (`analisis_planeacion_schedule`.`id` = \
    `analisis_planeacion_mo`.`schedule_id_id`) INNER JOIN `analisis_planeacion_workcenter` \
    ON (`analisis_planeacion_mo`.`workcenter_id_id` = `analisis_planeacion_workcenter`.`id`) \
    WHERE (NOT (`analisis_planeacion_schedule`.`eliminate_date` IS NOT NULL) AND \
    `analisis_planeacion_mo`.`schedule_id_id` IS NOT NULL AND `analisis_planeacion_mo`.`status` = 20) \
    GROUP BY `analisis_planeacion_schedule`.`id`ORDER BY NULL")
    return render(request, 'planning_log/list.html', {
        'schedules':schedules,
    })

def PlanningLogListDeteleted(request):
    mos = Mo.objects.values('schedule_id', 'project', 'schedule_id__number', 
                            'schedule_id__comments', 'schedule_id__mrr_date', 
                            'schedule_id__optiplan_date', 'workcenter_id__name'). \
                    annotate(Sum('order_qty')).\
                    filter(schedule_id__eliminate_date__isnull=False).\
                    order_by('-schedule_id__number')
    mos = mos.annotate(Sum('schedule_id'))
    return render(request, 'planning_log/list_deleted.html', {
        'mos':mos,
    })

def PlanningLogUpdateMrr(request, schedule_id):
    '''Update the date when the mrr is generated'''
    schedule = Schedule.objects.get(id=schedule_id)
    if schedule.mrr_date == None:
        schedule.mrr_date = datetime.now()
    else:
        schedule.mrr_date = None
    schedule.save()
    return redirect('planning_log_list')

def PlanningLogUpdateOptiplan(request, schedule_id):
    '''Update the date when the optiplan is generated'''
    schedule = Schedule.objects.get(id=schedule_id)
    if schedule.optiplan_date == None:
        schedule.optiplan_date = datetime.now()
    else:
        schedule.optiplan_date = None
    schedule.save()
    return redirect('planning_log_list')

def planning_log_resume(request):
    daily_resume_without_warehouse = Mo.objects.values('fiscal_date__year_number', 
                                                        'fiscal_date__month_name',
                                                        'fiscal_date__week_number', 
                                                        'fiscal_date__day_name').\
                                exclude(fiscal_date__year_number__isnull=True).\
                                annotate(total_pieces=Sum('order_qty')).\
                                order_by('fiscal_date__date')
    daily_resume_with_warehouse = Mo.objects.values('fiscal_date__year_number', 
                                                    'fiscal_date__month_name',
                                                    'fiscal_date__week_number', 
                                                    'fiscal_date__day_name', 
                                                    'workcenter_id__warehouse_id__name').\
                                            exclude(fiscal_date__year_number__isnull=True).\
                                            annotate(total_pieces=Sum('order_qty')).\
                                            order_by('fiscal_date__date')
    results_daily = []
    for item in daily_resume_without_warehouse:
        for item2 in daily_resume_with_warehouse:
            if (item['fiscal_date__year_number'] == item2['fiscal_date__year_number'] and
                item['fiscal_date__month_name'] == item2['fiscal_date__month_name'] and
                item['fiscal_date__week_number'] == item2['fiscal_date__week_number'] and 
                item['fiscal_date__day_name'] == item2['fiscal_date__day_name']):
                item['total_pieces_' + item2['workcenter_id__warehouse_id__name']] = item2['total_pieces']
        results_daily.append(item)
    
    weekly_resume_without_warehouse = Mo.objects.values('fiscal_date__year_number', 'fiscal_date__month_name',
                                        'fiscal_date__week_number').\
                                exclude(fiscal_date__year_number__isnull=True).\
                                annotate(total_pieces=Sum('order_qty')).\
                                order_by('fiscal_date__year_number', 'fiscal_date__month_name', 
                                        'fiscal_date__week_number')
    weekly_resume_with_warehouse = Mo.objects.values('fiscal_date__year_number', 'fiscal_date__month_name',
                                        'fiscal_date__week_number', 'workcenter_id__warehouse_id__name').\
                                exclude(fiscal_date__year_number__isnull=True).\
                                annotate(total_pieces=Sum('order_qty')).\
                                order_by('fiscal_date__year_number', 'fiscal_date__month_name', 
                                        'fiscal_date__week_number')
    results_weekly = []
    for item in weekly_resume_without_warehouse:
        for item2 in weekly_resume_with_warehouse:
            if (item['fiscal_date__year_number'] == item2['fiscal_date__year_number'] and
                item['fiscal_date__month_name'] == item2['fiscal_date__month_name'] and
                item['fiscal_date__week_number'] == item2['fiscal_date__week_number']):
                item['total_pieces_' + item2['workcenter_id__warehouse_id__name']] = item2['total_pieces']
        results_weekly.append(item)

    montly_resume_without_warehouse = Mo.objects.values('fiscal_date__year_number', 'fiscal_date__month_name').\
                                exclude(fiscal_date__year_number__isnull=True).\
                                annotate(total_pieces=Sum('order_qty')).\
                                order_by('fiscal_date__year_number', 'fiscal_date__month_name')
    montly_resume_with_warehouse = Mo.objects.values('fiscal_date__year_number', 'fiscal_date__month_name', 'workcenter_id__warehouse_id__name').\
                                exclude(fiscal_date__year_number__isnull=True).\
                                annotate(total_pieces=Sum('order_qty')).\
                                order_by('fiscal_date__year_number', 'fiscal_date__month_name')
    results_montly = []
    for item in montly_resume_without_warehouse:
        for item2 in montly_resume_with_warehouse:
            if (item['fiscal_date__year_number'] == item2['fiscal_date__year_number'] and
                item['fiscal_date__month_name'] == item2['fiscal_date__month_name']):
                item['total_pieces_' + item2['workcenter_id__warehouse_id__name']] = item2['total_pieces']
        results_montly.append(item)

    return render(request, 'planning_log/resume.html', {
        'results_daily': results_daily,
        'results_weekly':results_weekly,
        'results_montly':results_montly,
    })


def ConfirmDeleteSchedule(request, schedule_id):
    '''Add to the schedule a date deteleted and a comment'''
    schedule = Schedule.objects.get(id=schedule_id)
    if request.method == 'GET':
        form = FormSchedule(instance=schedule)
    else:
        form = FormSchedule(request.POST, instance=schedule)
        schedule.eliminate_date = datetime.now()
        schedule.save()
        form.save()
        return redirect('planning_log_list')
    return render(request, 'planning_log/delete.html', {'form':form})

def ReturnScheduleDeleted(request, schedule_id):
    '''Add to the schedule a date deteleted and a comment'''
    schedule = Schedule.objects.get(id=schedule_id)
    if request.method == 'GET':
        form = FormSchedule(instance=schedule)
    else:
        form = FormSchedule(request.POST, instance=schedule)
        schedule.eliminate_date = None
        schedule.save()
        form.save()
        return redirect('planning_log_list_deleted')
    return render(request, 'planning_log/delete.html', {'form':form})


def DeleteSchedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    schedule.eliminate_date = datetime.now()
    schedule.save()
    return redirect('planning_log_list')

def DetallesScheduleList(request, schedule_id):
    mos = Mo.objects.filter(schedule_id=schedule_id)
    return render(request, 'planning_log/detalles.html', {
        'mos':mos
    })

def AnalisisPlaneacionList(request):
    proposal_dict = None
    constraints = None 
    proposals = None
    if request.method == 'POST':
        constraint_value = request.POST.get('constraint')
        proposal_value = request.POST.get('proposal')
        workcenters = WorkCenter.objects.filter(constraint__period=constraint_value)
        workcenters = workcenters.values('name', 'line' , 'proposal__planner', 'constraint__status')
        workcenters = workcenters.annotate(Sum('proposal__grand_total')).\
                                annotate(pieces_goal= F('constraint__sah_goal') / F('constraint__sah_avg'))
        
        status_20 = Mo.objects.values('workcenter_id__name').\
                                filter(status='20').\
                                annotate(Sum('order_qty'), Sum('received_qty'))
        
        
        status_60 = Mo.objects.values('workcenter_id__name').\
                                filter(status='60').\
                                annotate(Sum('order_qty'), Sum('received_qty'))
        
        proposal_dict = [entry for entry in workcenters]
        status_20_dict = [entry2 for entry2 in status_20]
        status_60_dict = [entry3 for entry3 in status_60]
        for indice, value in enumerate(proposal_dict):
            try:
                for indice2, value in enumerate(status_20_dict):
                    if proposal_dict[indice]['name'] == status_20_dict[indice2]['workcenter_id__name']:
                        pieces_sts_20 = status_20_dict[indice2]['order_qty__sum'] + status_20_dict[indice2]['received_qty__sum']
                        proposal_dict[indice]['constraint__pieces_sts_20'] = pieces_sts_20
                        break
                    else:
                        proposal_dict[indice]['constraint__pieces_sts_20'] = 0
                
                for indice3, value in enumerate(status_60_dict):
                    if proposal_dict[indice]['name'] == status_60_dict[indice3]['workcenter_id__name']:
                        pieces_sts_60 = status_60_dict[indice3]['order_qty__sum'] + status_60_dict[indice3]['received_qty__sum']
                        proposal_dict[indice]['constraint__pieces_sts_60'] = pieces_sts_60
                        break
                    else:
                        proposal_dict[indice]['constraint__pieces_sts_60'] = 0
            except:
                pass
        constraints = Constraint.objects.values('period').annotate(Count('period'))[:5]
        proposals = Proposal.objects.values('name').annotate(Count('name'))[:5]


    else:
        workcenters = WorkCenter.objects.values('name', 'line' , 'proposal__planner', 'constraint__status', 
                                                'constraint__sah_avg', 'constraint__sah_goal').\
                                                annotate(Sum('constraint__id')).\
                                                annotate(Sum('proposal__grand_total')).\
                                                annotate(pieces_goal= F('constraint__sah_goal') / F('constraint__sah_avg'))
        
        status_20 = Mo.objects.values('workcenter_id__name').\
                                filter(status='20').\
                                annotate(Sum('order_qty'), Sum('received_qty'))
        status_60 = Mo.objects.values('workcenter_id__name').\
                                filter(status='60').\
                                annotate(Sum('order_qty'), Sum('received_qty'))
        
        proposal_dict = [entry for entry in workcenters]
        status_20_dict = [entry2 for entry2 in status_20]
        status_60_dict = [entry3 for entry3 in status_60]
        for indice, value in enumerate(proposal_dict):
            try:
                for indice2, value in enumerate(status_20_dict):
                    if proposal_dict[indice]['name'] == status_20_dict[indice2]['workcenter_id__name']:
                        pieces_sts_20 = status_20_dict[indice2]['order_qty__sum'] + status_20_dict[indice2]['received_qty__sum']
                        proposal_dict[indice]['constraint__pieces_sts_20'] = pieces_sts_20
                        break
                    else:
                        proposal_dict[indice]['constraint__pieces_sts_20'] = 0
                
                for indice3, value in enumerate(status_60_dict):
                    if proposal_dict[indice]['name'] == status_60_dict[indice3]['workcenter_id__name']:
                        pieces_sts_60 = status_60_dict[indice3]['order_qty__sum'] + status_60_dict[indice3]['received_qty__sum']
                        proposal_dict[indice]['constraint__pieces_sts_60'] = pieces_sts_60
                        break
                    else:
                        proposal_dict[indice]['constraint__pieces_sts_60'] = 0
            except:
                pass
        constraints = Constraint.objects.values('period').annotate(Count('period'))[:5]
        proposals = Proposal.objects.values('name').annotate(Count('name'))[:5]
    return render(request, 'analisis_planeacion/list.html', {
        'workcenters':proposal_dict,
        'constraints':constraints,
        'proposals':proposals,
        })

def WorkCenterList(request):
    '''Show all the list of workcenters availables'''
    workcenters = WorkCenter.objects.annotate(Sum('mo__order_qty'))
    return render(request, 'workcenter/list.html', {
        'workcenters':workcenters,
    })

def FabricShortageReport(request):
    if request.method == 'POST':
        initial_date = request.POST.get('initial_date')
        end_date = request.POST.get('end_date')
        results = FabricShortage.objects.filter(create_att__date__range=(initial_date, end_date))

        return render(request, 'shortage/reports.html', {
            'results':results
        })
    return render(request, 'shortage/reports.html')
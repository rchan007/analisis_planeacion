from django import forms
from .models import Constraint, Schedule, FabricShortage

class FormSchedule(forms.ModelForm):
    class Meta:
        model =  Schedule
        fields = [
            'comments',
        ]
        labels = {
            'comments': 'Comments',
        }
        widgets = {
            'comments':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Add your comments'})
        }

class FormFabricShortage(forms.ModelForm):
    class Meta:
        model =  FabricShortage
        fields = [
            'sku',
            'workcenter',
            'pcs_to_issue',
            'pcs_short',
            'no_fabric',
            'comments',
        ]
        labels = {
            'sku' : 'Sku',
            'workcenter': 'Workcenter',
            'pcs_to_issue': 'Pcs to issue',
            'pcs_short': 'Pcs Plan',
            'no_fabric':'Fabric',
            'comments': 'Comments',

        }
        widgets = {
            'sku': forms.Select(),
            'workcenter': forms.Select(),
            'pcs_to_issue': forms.NumberInput(),
            'pcs_short': forms.NumberInput(),
            'no_fabric': forms.TextInput(),
            'comments': forms.TextInput(),
        }

class FormConstraint(forms.ModelForm):
    class Meta:
        model =  Constraint
        fields = [
            'period',
            'status',
            'sah_avg',
            'sah_goal',
            'workcenter_id',
            'comments',
        ]
        labels = {
            'period':'Period',
            'status':'Status',
            'sah_avg':'Sah Avg',
            'sah_goal': 'Sah Goal',
            'workcenter_id': 'Workcenter',
            'comments': 'Comments',
        }
        widgets = {
            'period':forms.TextInput(attrs={'class':'form-control'}),
            'status':forms.TextInput(attrs={'class':'form-control'}),
            'sah_avg':forms.NumberInput(attrs={'class':'form-control', 'id':'sah_avg'}),
            'sah_goal':forms.NumberInput(attrs={'class':'form-control', 'id':'sah_goal'}),
            'workcenter_id':forms.Select(attrs={'class':'form-control'}),
            'comments': forms.Textarea(attrs={'class':'form-control'}),
        }
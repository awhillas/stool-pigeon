from django import forms
from .models import StoolRecord


class StoolRecordForm(forms.ModelForm):
    class Meta:
        model = StoolRecord
        fields = ['stool_type', 'pain', 'blood_in_stool', 'blood_on_paper']
        widgets = {
            'stool_type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'pain': forms.CheckboxInput(attrs={
                'class': 'form-check-input health-indicator-check',
                'role': 'switch'
            }),
            'blood_in_stool': forms.CheckboxInput(attrs={
                'class': 'form-check-input health-indicator-check', 
                'role': 'switch'
            }),
            'blood_on_paper': forms.CheckboxInput(attrs={
                'class': 'form-check-input health-indicator-check',
                'role': 'switch'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set labels for better accessibility
        self.fields['pain'].label = 'Pain'
        self.fields['blood_in_stool'].label = 'Blood in stool'
        self.fields['blood_on_paper'].label = 'Blood on paper'
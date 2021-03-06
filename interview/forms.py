# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row
from django import forms
from models import Interview
import re

class FormInterview(forms.Form):
    """
    Dynamic form creator class
    """
    regex = re.compile(r'\s*,\s*')

    def radio_sel_choices(self, choices_str):
        choices = self.regex.split(choices_str)
        choices_tuple = [(choice, choice) for choice in choices]
        return choices_tuple

    def __init__(self, elemslist, *args, **kwargs):
        super(FormInterview, self).__init__(*args, **kwargs)

        # import pdb
        # pdb.set_trace()
        list_fields = []
        for elem in elemslist:
            list_fields.append(str(elem.id))

            if elem.type_elem == 'txt':
                 self.fields[str(elem.id)] = forms.CharField(label=elem.text_before_elem, max_length=200,
                                                        initial=elem.default_value, help_text=elem.text_after_elem)
            elif elem.type_elem == 'select':
                CHOICES = self.radio_sel_choices(elem.radio_select_values)
                self.fields[str(elem.id)] = forms.ChoiceField(choices=CHOICES, label=elem.text_before_elem,
                                                         help_text=elem.text_after_elem)
            elif elem.type_elem == 'mselect':
                CHOICES = self.radio_sel_choices(elem.radio_select_values)
                self.fields[str(elem.id)] = forms.MultipleChoiceField(choices=CHOICES, label=elem.text_before_elem,
                                                                 help_text=elem.text_after_elem, initial='1')
            elif elem.type_elem == 'radio':
                CHOICES = self.radio_sel_choices(elem.radio_select_values)
                self.fields[str(elem.id)] = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES,
                                                         label=elem.text_before_elem, help_text=elem.text_after_elem)
            elif elem.type_elem == 'check':
                self.fields[str(elem.id)] = forms.BooleanField(label=elem.text_before_elem, required=False,
                                                               help_text=elem.text_after_elem)
            elif elem.type_elem == 'dpicker':

                bottom, top = self.regex.split(elem.top_bottom_values)
                self.fields[str(elem.id)] = forms.CharField(label=elem.text_before_elem,
                                                       widget=forms.NumberInput(attrs={'min': bottom, 'max': top}),
                                                       help_text=elem.text_after_elem, initial=elem.default_value)
        # super(FormInterview, self).__init__(*args, **kwargs)


    # def save(self):
    #     pass

class FormEditInterview(forms.ModelForm):
    create_date = forms.DateTimeField(widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'))
    class Meta:
        model = Interview
        fields = '__all__'
        # localized_fields = ('create_date', )


# -*- coding: utf-8 -*-
from ckan.common import _
import ckan.logic.validators as validators

def required(errors, error_summary, label, form_name, value):
    if not value:
        errors[form_name] = [label + u'は必須項目です']
        error_summary[label] = u'必須入力です'
    return True

def requiredCheckbox(errors, error_summary, label, form_name, value):
    if not value:
        errors[form_name] = [label + u'を１つ以上選択してください']
        error_summary[label] = u'１つ以上選択してください'

def maxLength(errors, error_summary, label, form_name, value, max_length):
    if not value:
        return
    
    if len(value) > max_length:
        errors[form_name] = [label + u'は' + str(max_length) + u'文字以下で入力してください']
        error_summary[label] = str(max_length) + u'文字以下で入力してください'

def emailAddress(errors, error_summary, label, form_name, value):
    if not value:
        return

    try:
        validators.email_validator(value, None)
        return
    except:
        errors[form_name] = [_('Email {email} is not a valid format').format(email=value)]
        error_summary[label] = _('Email {email} is not a valid format').format(email=value)
    

def checkboxAndRequired(errors, error_summary, label, form_name, value, check_list):
    if len(check_list) == 0:
        return
    
    if label in check_list and not value:
        errors[form_name] = [label + u'選択時は必須項目です' ]
        error_summary[label] = label + u'選択時は必須項目です'


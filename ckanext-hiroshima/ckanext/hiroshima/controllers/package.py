# -*- coding: utf-8 -*-

from ckan.controllers.package import PackageController
from ckan.common import c, _, request, config
from collections import OrderedDict
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.model as model
import ckan.logic as logic
import uuid
import json

from ckanext.hiroshima.model import requests
from ckanext.hiroshima.lib import mailer
from ckanext.hiroshima.lib import validators
from ckanext.hiroshima.lib import fiware
from ckanext.hiroshima.plugin import data_request_license_id, questionnaire_license_id, meta_data_request_license_id

get_action = logic.get_action
_get_or_bust = logic.get_or_bust
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized

class HiroshimaPackageController(PackageController):

    def _getDataRequest(self, license_id):
        self.checkLicense(data_request_license_id(), license_id)

        errors = {}
        error_summary = OrderedDict()
        form_data = {}

        extra_vars = {u'errors': errors,
                      u'error_summary': error_summary,
                      u'form_data': form_data}
        return toolkit.render('package/data-request.html', extra_vars=extra_vars)

    def _postDataRequest(self, id, resource_id):
        package_id = id
        purposes = self.requestParamsArray('purposes[]')
        other_purpose = request.params.get('other-purpose')
        participation_consent = request.params.get('participation-consent')
        participation_already = request.params.get('participation-already')
        name = request.params.get('staff-name')
        email = request.params.get('email-address')
        company = request.params.get('company-name')
        
        errors = {}
        error_summary = OrderedDict()
        form_data = {}

        validators.requiredCheckbox(errors, error_summary, u'利用目的', 'purposes[]', purposes)
        validators.checkboxAndRequired(errors, error_summary, u'その他の利用', 'other-purpose', other_purpose, purposes)
        validators.maxLength(errors, error_summary, u'その他の利用', 'other-purpose', other_purpose, 255)
        validators.required(errors, error_summary, u'規約の同意', 'participation-consent', participation_consent)
        validators.required(errors, error_summary, u'参加済み', 'participation-already', participation_already)
        validators.required(errors, error_summary, u'会社名', 'company-name', company)
        validators.maxLength(errors, error_summary, u'会社名', 'company-name', company, 255)
        validators.required(errors, error_summary, u'担当者名', 'staff-name', name)
        validators.maxLength(errors, error_summary, u'担当者名', 'staff-name', name, 255)
        validators.required(errors, error_summary, u'連絡先メールアドレス', 'email-address', email)
        validators.emailAddress(errors, error_summary, u'連絡先メールアドレス', 'email-address', email)
        validators.maxLength(errors, error_summary, u'連絡先メールアドレス', 'email-address', email, 255)

        if errors:
            form_data['company-name'] = company
            form_data['staff-name'] = name
            form_data['email-address'] = email
            form_data['other-purpose'] = other_purpose
            form_data['purposes[]'] = purposes
            form_data['participation-consent'] = participation_consent
            form_data['participation-already'] = participation_already

            extra_vars = {u'errors': errors,
                          u'error_summary': error_summary,
                          u'form_data': form_data}
            return toolkit.render('package/data-request.html', extra_vars=extra_vars)

        request_data = []
        if u'その他の利用' in purposes:
            self.appendFormData(request_data, u'その他の利用', 'other-purpose')

        self.appendFormData(request_data, u'利用目的', 'purposes[]')
        self.appendFormData(request_data, u'規約の同意', 'participation-consent')
        self.appendFormData(request_data, u'ひろしまサンドボックス推進協議会への参加確認', 'participation-already')
        self.appendFormData(request_data, u'会社名', 'company-name')

        obj = requests.Requests(package_id,
                                resource_id,
                                requests.STATE_MAIL_UNSENT, 
                                name, 
                                email, 
                                json.dumps(request_data, ensure_ascii=False)
                                )

        try:
            session = model.Session
            session.add(obj)
            session.commit()
        except:
            session.rollback()
            toolkit.abort(500, 'Database Error')

        return toolkit.redirect_to('package.complete-request', id=_get_or_bust(c.pkg_dict, 'name'), resource_id=resource_id, answered=True)

    def _getQuestionnaire(self, license_id):
        self.checkLicense(questionnaire_license_id(), license_id)

        errors = {}
        error_summary = OrderedDict()
        form_data = {}

        extra_vars = {u'errors': errors,
                      u'error_summary': error_summary,
                      u'form_data': form_data}
        return toolkit.render('package/questionnaire.html', extra_vars=extra_vars)

    def _postQuestionnaire(self, id, resource_id):
        package_id = id
        purposes = self.requestParamsArray('purposes[]')
        other_purpose = request.params.get('other-purpose')

        if request.params.get('skip'):
            return toolkit.redirect_to('package.complete-request', id=_get_or_bust(c.pkg_dict, 'name'), resource_id=resource_id, answered=False)

        errors = {}
        error_summary = OrderedDict()
        form_data = {}
        
        validators.requiredCheckbox(errors, error_summary, u'利用目的', 'purposes[]', purposes)
        validators.checkboxAndRequired(errors, error_summary, u'その他の利用', 'other-purpose', other_purpose, purposes)
        validators.maxLength(errors, error_summary, u'その他の利用', 'other-purpose', other_purpose, 255)

        if errors:
            form_data['other-purpose'] = other_purpose
            form_data['purposes[]'] = purposes

            extra_vars = {u'errors': errors,
                          u'error_summary': error_summary,
                          u'form_data': form_data}
            return toolkit.render('package/questionnaire.html', extra_vars=extra_vars)

        request_data = []
        self.appendFormData(request_data, u'その他の利用', 'other-purpose')
        self.appendFormData(request_data, u'利用目的', 'purposes[]')

        obj = requests.Requests(package_id, 
                                resource_id,
                                requests.STATE_MAIL_UNSENT, 
                                None, 
                                None, 
                                json.dumps(request_data, ensure_ascii=False)
                                )

        try:
            session = model.Session
            session.add(obj)
            session.commit()
        except:
            session.rollback()
            toolkit.abort(500, 'Database Error')

        return toolkit.redirect_to('package.complete-request', id=_get_or_bust(c.pkg_dict, 'name'), resource_id=resource_id, answered=True)

    def _getMetaDataRequest(self, license_id):
        self.checkLicense(meta_data_request_license_id(), license_id)
        
        errors = {}
        error_summary = OrderedDict()
        form_data = {}

        extra_vars = {u'errors': errors,
                      u'error_summary': error_summary,
                      u'form_data': form_data}
        return toolkit.render('package/meta_data_request.html', extra_vars=extra_vars)

    def _postMetaDataRequest(self, id):
        package_id = id
        purpose = request.params.get('purpose')
        participation_already = request.params.get('participation-already')
        name = request.params.get('staff-name')
        email = request.params.get('email-address')
        company = request.params.get('company-name')
        
        errors = {}
        error_summary = OrderedDict()
        form_data = {}

        validators.required(errors, error_summary, u'参加済み', 'participation-already', participation_already)
        validators.required(errors, error_summary, u'利用目的', 'purpose', purpose)
        validators.maxLength(errors, error_summary, u'利用目的', 'purpose', purpose, 1024)
        validators.required(errors, error_summary, u'会社名', 'company-name', company)
        validators.maxLength(errors, error_summary, u'会社名', 'company-name', company, 255)
        validators.required(errors, error_summary, u'担当者名', 'staff-name', name)
        validators.maxLength(errors, error_summary, u'担当者名', 'staff-name', name, 255)
        validators.required(errors, error_summary, u'連絡先メールアドレス', 'email-address', email)
        validators.emailAddress(errors, error_summary, u'連絡先メールアドレス', 'email-address', email)
        validators.maxLength(errors, error_summary, u'連絡先メールアドレス', 'email-address', email, 255)

        if errors:
            form_data['company-name'] = company
            form_data['staff-name'] = name
            form_data['email-address'] = email
            form_data['purpose'] = purpose
            form_data['participation-already'] = participation_already

            extra_vars = {u'errors': errors,
                          u'error_summary': error_summary,
                          u'form_data': form_data}
            return toolkit.render('package/meta_data_request.html', extra_vars=extra_vars)

        request_data = []
        self.appendFormData(request_data, u'利用目的', 'purpose')
        self.appendFormData(request_data, u'ひろしまサンドボックス推進協議会への参加確認', 'participation-already')
        self.appendFormData(request_data, u'会社名', 'company-name')

        obj = requests.Requests(package_id,
                                None,
                                requests.STATE_MAIL_UNSENT, 
                                name, 
                                email, 
                                json.dumps(request_data, ensure_ascii=False)
                                )

        try:
            session = model.Session
            session.add(obj)
            session.commit()
        except:
            session.rollback()
            toolkit.abort(500, 'Database Error')

        try:
            mailer.send_confirm_mail_address(name, email, obj.token)
        except:
            h.flash_error(_(u'Error sending the email. Try again later '
                                'or contact an administrator for help'))
            return h.redirect_to(controller='package',
                                 action='read',
                                 id=_get_or_bust(c.pkg_dict, 'name')
                                 )

        extra_vars = {u'email_address': email}
        return toolkit.render('package/applying.html', extra_vars=extra_vars)

    def dataRequest(self, id, resource_id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}

        data_dict = {'id': id, 'include_tracking': True}
        resource_dict = get_action('resource_show')(context,
                                                    {'id': resource_id})
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            c.resource = resource_dict
        except (NotFound, NotAuthorized):
            # dataset not exist, not authorized
            toolkit.abort(404, _('Dataset not found'))

        if request.method == 'POST':
            return self._postDataRequest(_get_or_bust(c.pkg_dict, 'id'), _get_or_bust(c.resource, 'id'))

        return self._getDataRequest(_get_or_bust(c.pkg_dict, 'license_id'))

    def requestList(self, id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}

        data_dict = {'id': id, 'include_tracking': True}

        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except (NotFound, NotAuthorized):
            # dataset not exist, not authorized
            toolkit.abort(404, _('Dataset not found'))

        license_id = _get_or_bust(c.pkg_dict, 'license_id')
        isAdmin = c.userobj.sysadmin
        if not isAdmin and license_id != meta_data_request_license_id() and license_id != data_request_license_id() and license_id != questionnaire_license_id():
            return h.redirect_to(controller='package',
                                 action='read',
                                 id=_get_or_bust(c.pkg_dict, 'name')
                                 )

        package_id = _get_or_bust(c.pkg_dict, 'id')
        page = h.get_page_number(request.params)
        limit = int(config.get('ckan.datasets_per_page', 10))
        data = requests.Requests.by_dataset(package_id, limit, (page - 1) * limit)

        request_list = []
        for item in data:
            request_data = json.loads(item.request_data)
            purposes = filter(lambda value: value[u'key'] == u'利用目的', request_data)
            resource = None
            if item.resource_id is not None:
                resource_dict = get_action('resource_show')(context,
                                                            {'id': item.resource_id})
                resource = resource_dict[u'name']

            request_list.append({
                'datetime': item.created.strftime("%Y/%m/%d %H:%M:%S"),
                'mail_sent': item.state,
                'name': item.name,
                'mail': item.email_address,
                'resource': resource,
                'purposes': purposes[0][u'values']
            })

        c.page = h.Page(
            collection=request_list,
            page=page,
            item_count=requests.Requests.request_count(package_id),
            items_per_page=limit
        )
        c.page.items = request_list

        return toolkit.render('package/request_list.html')

    def complete(self, token):
        data = requests.Requests.by_token(token)
        if data == None:
            toolkit.abort(404, u'URLが一致しません')

        if data.state == requests.STATE_MAIL_SENT:
            toolkit.abort(403, u'申込済みです')

        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}

        data_dict = {'id': data.package_id, 'include_tracking': True}
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except (NotFound, NotAuthorized):
            # dataset not exist, not authorized
            toolkit.abort(404, _('Dataset not found'))

        user_name = data.name
        user_email = data.email_address
        package_id = _get_or_bust(c.pkg_dict, 'id')
        consortium_name = _get_or_bust(c.pkg_dict, 'author')
        consortium_email = _get_or_bust(c.pkg_dict, 'author_email')
        try:
            mailer.send_request_to_other_consortium(user_name, user_email, _get_or_bust(c.pkg_dict, 'name'), consortium_name, consortium_email)
        except:
            h.flash_error(_(u'Error sending the email. Try again later '
                                'or contact an administrator for help'))
            return h.redirect_to(controller='package',
                                 action='read',
                                 id=_get_or_bust(c.pkg_dict, 'name')
                                 )

        try:
            data.update_status()
        except:
            toolkit.abort(500, 'Database Error')

        extra_vars = {u'token': token}
        return toolkit.render('package/complete.html', extra_vars=extra_vars)

    def questionnaire(self, id, resource_id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}

        data_dict = {'id': id, 'include_tracking': True}
        resource_dict = get_action('resource_show')(context,
                                                    {'id': resource_id})
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            c.resource = resource_dict
        except (NotFound, NotAuthorized):
            # dataset not exist, not authorized
            toolkit.abort(404, _('Dataset not found'))

        if request.method == 'POST':
            return self._postQuestionnaire(_get_or_bust(c.pkg_dict, 'id'), _get_or_bust(c.resource, 'id'))

        return self._getQuestionnaire(_get_or_bust(c.pkg_dict, 'license_id'))

    def metaDataRequest(self, id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}

        data_dict = {'id': id, 'include_tracking': True}

        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
        except (NotFound, NotAuthorized):
            # dataset not exist, not authorized
            toolkit.abort(404, _('Dataset not found'))

        if request.method == 'POST':
            return self._postMetaDataRequest(_get_or_bust(c.pkg_dict, 'id'))

        return self._getMetaDataRequest(_get_or_bust(c.pkg_dict, 'license_id'))

    def completeRequest(self, id, resource_id):
        if not toolkit.request.GET.has_key('answered'):
            toolkit.abort(404, u'URLが一致しません')

        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}

        data_dict = {'id': id, 'include_tracking': True}

        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            resource_dict = get_action('resource_show')(context,
                                                        {'id': resource_id})
            c.resource = resource_dict
        except (NotFound, NotAuthorized):
            # dataset not exist, not authorized
            toolkit.abort(404, _('Dataset not found'))

        extra_vars = {u'answered': toolkit.asbool(toolkit.request.GET.get('answered'))}

        return toolkit.render('package/download.html', extra_vars=extra_vars)

    def appendFormData(self, array, key, form_name):
        if not request.params.has_key(form_name):
            return

        params_array = self.requestParamsArray(form_name)

        if not params_array:
            return

        array.append({'key': key,
                      'values': params_array})

    def requestParamsArray(self, form_name):
        if not request.params.has_key(form_name):
            return []

        values = []
        for (param, value) in request.params.items():
            if param == form_name and value:
                values.append(value)
        return values

    def checkLicense(self, expected, actual):
        if actual != expected:
            h.flash_error(u'不正なリクエストです')
            return h.redirect_to(controller='package',
                                 action='read',
                                 id=_get_or_bust(c.pkg_dict, 'name')
                                 )
        return True

    def fiware(self, type, id, attrName):
        values = fiware.getdata(type, id, attrName)
        return values


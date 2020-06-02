# -*- coding: utf-8 -*-

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from routes.mapper import SubMapper
from ckan.lib.plugins import DefaultTranslation
from ckan.common import config, c
from ckan.plugins.toolkit import Invalid
import ckan.model as model

def iot_canvas_url():
    return config.get('ckan.hiroshima.iot_canvas_url')

def hiroshima_prefecture_url():
    return config.get('ckan.hiroshima.prefecture_url')

def hiroshima_sandbox_url():
    return config.get('ckan.hiroshima.sandbox_url')

def data_request_license_id():
    return 'hiroshima-sandbox'

def questionnaire_license_id():
    return 'cc-by-jp'

def meta_data_request_license_id():
    return 'none'

def required_for_nolicense(key, flattened_data, errors, context):
    license_id = flattened_data.get(('license_id',), None)
    value = flattened_data.get(key)

    if license_id == meta_data_request_license_id() and not value:
        raise Invalid(u'No License(Sample)選択時は必須項目です')
    return value

class HiroshimaPlugin(plugins.SingletonPlugin, DefaultTranslation, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IValidators)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'hiroshima')

    def get_helpers(self):
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'iot_canvas_url': iot_canvas_url,
            'hiroshima_prefecture_url': hiroshima_prefecture_url,
            'hiroshima_sandbox_url': hiroshima_sandbox_url,
            'data_request_license_id': data_request_license_id,
            'questionnaire_license_id': questionnaire_license_id,
            'meta_data_request_license_id': meta_data_request_license_id
            }

    def before_map(self, map):
        m = SubMapper(
            map,
            controller='ckanext.hiroshima.controllers.home:\
                HiroshimaHomeController')
        # Connect routes for usepolicy
        m.connect('home.usepolicy','/usepolicy', #route,URL,action
            action="usePolicy")
        m.connect('home.opinion','/opinion',
            action="opinion")
        m.connect('home.about-use','/about-use',
            action="aboutUse")
        m.connect('home.index','/',
            action="index")

        # /user/register
        map.connect('/user/register',
                    controller='ckanext.hiroshima.controllers.user:HiroshimaUserController',
                    action='register')

        # /dataset/data-request
        map.connect('package.data-request',
                    '/dataset/{id}/resource/{resource_id}/data-request',
                    controller='ckanext.hiroshima.controllers.package:HiroshimaPackageController',
                    action='dataRequest')

        # /dataset/questionnaire
        map.connect('package.questionnaire',
                    '/dataset/{id}/resource/{resource_id}/questionnaire',
                    controller='ckanext.hiroshima.controllers.package:HiroshimaPackageController',
                    action='questionnaire')

        # /dataset/meta-data-request
        map.connect('package.meta-data-request',
                    '/dataset/{id}/meta-data-request',
                    controller='ckanext.hiroshima.controllers.package:HiroshimaPackageController',
                    action='metaDataRequest',
                    ckan_icon='pencil-square-o')

        # /dataset/request-list
        map.connect('package.request-list',
                    '/dataset/request-list/{id}',
                    controller='ckanext.hiroshima.controllers.package:HiroshimaPackageController',
                    action='requestList',
                    ckan_icon='list')

        # /dataset/complete
        map.connect('package.complete',
                    '/dataset/complete/{token}',
                    controller='ckanext.hiroshima.controllers.package:HiroshimaPackageController',
                    action='complete')

        # /dataset/complete-request
        map.connect('package.complete-request',
                    '/dataset/{id}/resource/{resource_id}/complete-request',
                    controller='ckanext.hiroshima.controllers.package:HiroshimaPackageController',
                    action='completeRequest')

        # /fiware
        map.connect('fiware',
                    '/fiware/{type}/{id}/{attrName}',
                    controller='ckanext.hiroshima.controllers.package:HiroshimaPackageController',
                    action='fiware')

        return map

    # IValidators
    def get_validators(self):
        return {'required_for_nolicense': required_for_nolicense}

    # IDatasetForm
    def _modify_package_schema(self, schema):
        schema.update({
            'author': [toolkit.get_validator('required_for_nolicense')],
            'author_email': [toolkit.get_validator('required_for_nolicense'),
                            toolkit.get_validator('email_validator')]
        })
        return schema

    def create_package_schema(self):
        schema = super(HiroshimaPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)

        return schema

    def update_package_schema(self):
        schema = super(HiroshimaPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)

        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []

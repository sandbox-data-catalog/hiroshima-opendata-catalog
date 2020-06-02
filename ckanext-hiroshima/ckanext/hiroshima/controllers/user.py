from ckan.controllers.user import UserController
import ckan.lib.base as base
import ckan.model as model
import ckan.lib.helpers as h
import ckan.authz as authz
from ckan.common import _, c, request, response
import ckan.logic as logic

check_access = logic.check_access
render = base.render
NotAuthorized = logic.NotAuthorized

class HiroshimaUserController(UserController):
    def register(self, data=None, errors=None, error_summary=None):
        context = {'model': model, 'session': model.Session, 'user': c.user,
                   'auth_user_obj': c.userobj}
        try:
            check_access('user_create', context)
        except NotAuthorized:
            h.redirect_to(u'user.login')

        return self.new(data, errors, error_summary)


    def new(self, data=None, errors=None, error_summary=None):
        '''GET to display a form for registering a new user.
           or POST the form data to actually do the user registration.
        '''
        context = {'model': model,
                   'session': model.Session,
                   'user': c.user,
                   'auth_user_obj': c.userobj,
                   'schema': self._new_form_to_db_schema(),
                   'save': 'save' in request.params}

        try:
            check_access('user_create', context)
        except NotAuthorized:
            h.redirect_to(u'user.login')

        if context['save'] and not data and request.method == 'POST':
            return self._save_new(context)

        if c.user and not data and not authz.is_sysadmin(c.user):
            # #1799 Don't offer the registration form if already logged in
            return render('user/logout_first.html')

        form_vars = {
            u'data': data or {},
            u'errors': errors or {},
            u'error_summary': error_summary or {}
        }

        extra_vars = {
            u'is_sysadmin': authz.is_sysadmin(c.user),
            u'form': render(self.new_user_form, form_vars)
        }
        return render(u'user/new.html', extra_vars)

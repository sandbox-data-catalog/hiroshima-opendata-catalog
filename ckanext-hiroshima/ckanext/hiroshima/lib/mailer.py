import ckan.plugins.toolkit as toolkit
import ckan.lib.mailer as mailer
from ckan.common import config

def send_confirm_mail_address(user_name, email, token):
    host = config['ckan.host']
    mail_extra_vars = {
        'name': user_name,
        'link': 'http://' + host + '/dataset/complete/' + str(token)
    }
    try:
        mailer.mail_recipient(
            recipient_name = None,
            recipient_email = email,
            subject = toolkit.render('mail/request_data_subject.txt', {}),
            body = toolkit.render('mail/request_data.txt', mail_extra_vars),
            headers = [])
    except mailer.MailerException:
        raise

def send_request_to_other_consortium(user_name, user_email, package_id, consortium_name, consortium_email):
    host = config['ckan.host']
    mail_extra_vars = {
        'user_name': user_name,
        'user_email': user_email,
        'consortium_name': consortium_name,
        'link': 'http://' + host + '/dataset/' + str(package_id)
    }
    headers = {}
    cc_email = config.get('smtp.mail_cc')
    if cc_email:
        headers['Cc'] = u"%s" % (cc_email)

    try:
        mailer.mail_recipient(
            recipient_name = None,
            recipient_email = consortium_email,
            subject = toolkit.render('mail/request_consortium_subject.txt', {}),
            body = toolkit.render('mail/request_consortium.txt', mail_extra_vars),
            headers = headers)
    except mailer.MailerException:
        raise

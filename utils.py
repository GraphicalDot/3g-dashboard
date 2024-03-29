import smtplib
from email.mime.text import MIMEText
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.utils.text import slugify

import inspect


def uuid_name_definition(parent, str_uuid):
    """
    :param parent:
    :param str_uuid:
    :return: A uuid string of full branch( call from models local function)
    """
    return (parent.get_uuid_name_definition() + " | " + str_uuid).lower()


def name_definition(title, parent):
    return (str(parent)+" | "+title).lower()


def get_permission_name(instance):
    return 'crud | '+str(instance)

# from g3_dashboard import  settings

# import requests
# def send_simple_mail():
#     return requests.post(
#         "https://api.mailgun.net/v3/sandbox3c2172091a0d419e867ec7bf45185cdb.mailgun.org/messages",
#         auth=("api", "key-3d91be5330422b6a78f9e9d859010763"),
#         data={"from": "Mailgun Sandbox <postmaster@sandbox3c2172091a0d419e867ec7bf45185cdb.mailgun.org>",
#               "to": "gaurav <gaurav@madmachines.io>",
#               "subject": "Hello gaurav",
#               "text": "Congratulations gaurav, you just sent an email with "
#                       "Mailgun!  You are truly awesome!  You can see a record of this email in your "
#                       "logs: https://mailgun.com/cp/log .  You can send up to 300 emails/day from this "
#                       "sandbox server.  Next, you should add your own domain so you can send 10,000 "
#                       "emails/month for free."})


def send_mail(to, subject, msg_body, password=None):
    """
    Call to send email on users email address
    :param to:
    :param subject:
    :param msg_body:
    :param password:
    :return: True is user mail is send success
    """
    if password:
        msg_content = msg_body
        message = MIMEText(msg_content, 'html')

        message['From'] = '3G DashBoard <sender@server>'
        message['To'] = to
        message['Cc'] = 'Gaurav Tyagi <gaurav@madmachines.io>'
        message['Subject'] = subject

        msg_full = message.as_string()

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        try:
            server.login('gaurav@madmachines.io', password)
            server.sendmail('gaurav@madmachines.io',
                            ['grvtyagi22@gmail.com'],
                            msg_full)
        except Exception as e:
            print(e.args)
        finally:
            server.quit()


def create_object_permission(app_label, model_name, per_codename, per_name, uuid_codename):
    """
    Create permission on every object creations ...
    """
    content_type = ContentType.objects.get(app_label=app_label.lower(), model=model_name.lower())
    permission = Permission.objects.get_or_create(
        # name=per_name.lower(),
        uuid_codename=uuid_codename,
        defaults={
                  # 'uuid_codename': uuid_codename,
                  'name': per_name.lower(),
                  'content_type': content_type,
                  'codename': per_codename.lower()
                  }
        )

    return permission


def create_slug(sender, instance, new_slug=None):
    """
    Recursive function to check duplicate slug and create new slug from instance title.
    :param sender:
    :param instance:
    :param new_slug:
    :return:
    """
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = sender.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = '%s-%s' %(slug, qs.count())
        return create_slug(sender, instance, new_slug=new_slug)
    return slug


def add_current_objects_parent_to_request_session(sender, instance, **kwargs):
    """
    :param sender:
    :param instance:
    :param kwargs:
    :return: Save objects code on pre_save
             class data for get its parent's code when initialize form drop down.
    """
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    if request:
        request.session['LS:'+sender.__name__] = str(instance.code)

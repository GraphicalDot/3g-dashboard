from django.contrib.auth.models import Permission
from constants import mail_template_constants

from utils import get_log_msg


def update_user(sender, instance, **kwargs):
    """
    Call when user permissions change via admin
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when user update
    """
    # Post add of permission.
    if kwargs.get('action', None) == 'post_add':
        try:
            permissions = Permission.objects.filter(user=instance)
            # TODO: Call api when update user permissions
        except Exception as e:
            print('Update user signal ---', e.args)
    else:
        print(instance, 'pre add call')


def update_permission_if_obj_update(sender, instance, **kwargs):
    """
    On any-object update, change their relative permission name
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    # try:
    #     old = sender.objects.get(pk=instance.code)
    #     if not get_permission_name(instance) == get_permission_name(old):
    #         print('change in permission ...', get_permission_name(old))
    #         uuid_codename = old.get_uuid_name_definition()
    #         all_related_permissions = Permission.objects.filter(uuid_codename__icontains=uuid_codename)
    #         # permission = Permission.objects.get(name=get_permission_name(old))
    #         for permission in all_related_permissions:
    #             # permission.name = get_permission_name(instance)
    #             # permission.codename = str(instance).lower()
    #             # permission.save()
    #             print(permission.name)
    #             print(sender.__name__, PERMISSION_NAME_FORMAT.index(sender.__name__))
    #             print(permission.name.split(' | ')[PERMISSION_NAME_FORMAT.index(sender.__name__)])
    #     else:
    #         print('No Change in permission ...')
    #
    # except Exception as e:
    #     print(e.args)
    pass


# def update_user_group(sender, instance, **kwargs):
#     print('-------- When assign group ------')
#     print(kwargs)
#     if type(instance).__name__ == 'Group':
#         print(instance.permissions.all())
#     elif type(instance).__name__ == 'MyUser' and kwargs.get('action') == 'post_add':
#         print(instance.groups.all())
#         for group in instance.groups.all():
#             # print(group)
#             for permission in group.permissions.all():
#                 print(permission.id, instance.id)
#     # add_permission_to_user_from_group(5, 90)
#                 # print(instance.user_permissions.add(permission).query)
#                 # TO-DO Call a raw sql query for add permissions to user
#                 # otherwise create a call-hell via signals ..


def change_user_type(sender, instance, **kwargs):
    """
    Change type of user
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """

    if instance.is_superuser:
        instance.type = 'SUPER-ADMIN'
    elif instance.is_staff:
        instance.type = 'ADMIN'
    else:
        if instance.type in ['ADMIN', 'SUPER-ADMIN']:
            instance.type = 'DEFAULT'
    print('update/create user call ...')


def delete_uploader(sender, instance, **kwargs):
    """
    On uploader delete set admins value to default
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.user.type = 'DEFAULT'
    instance.user.save()


def send_mail_on_user_create(sender, instance, **kwargs):
    """
    Call on post_save when user create
    :param sender:
    :param instance:
    :param kwargs:
    :return: Send an email on created user's email field.
    """
    register_subject = mail_template_constants.RESISTER_MSG.get('SUBJECT')
    register_body_template = mail_template_constants.RESISTER_MSG.get('MSG_BODY')
    register_body_template = register_body_template.format(user_name=instance.username, password=instance.password)
    # send_mail(instance.email, register_subject, register_body_template)


def change_log_msg(sender, instance, **kwargs):
    # msg = "Has been changed by {user}".\
    #     format(**{'user': instance.user})
    get_log_msg(instance, **kwargs)

from django.contrib.auth.models import Permission
from utils import create_object_permission

from utils import create_slug, get_permission_name
from django.utils.text import slugify


def create_user_to_uploader(sender, instance, **kwargs):
    """
    Call when user set as uploader changes via admin
    :param sender:
    :param instance:
    :param kwargs:
    :return: Callback Api function when user update
    """
    if not instance.user.is_staff:
        instance.user.type = 'UPLOADER'
        instance.user.save()
    else:
        print('Admin or Super-Admin can not be a uploader ...')

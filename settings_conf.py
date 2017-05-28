# ///////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\////////////////
# \\\\\\\\\\\\\\\Call to override on permissions////////////////
# \\\\\\\\\\\\\\\///////////////////////////////\\\\\\\\\\\\\\\\

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from django.db import models
from constants.global_constant import PERMISSION_CODENAME_FORMAT
from django.contrib.auth import get_user_model

ContentType._meta.get_field("app_label").max_length = 1000
Permission._meta.get_field("codename").max_length = 1000


def custom(self):
    def __get_permission_name(perm, curr_instance):
        return perm.content_type.model + ' | ' + str(curr_instance)

    if self.uuid_codename:
        __Class = PERMISSION_CODENAME_FORMAT.get(self.content_type.model, None)
        if __Class:
            instance = __Class.objects.get(pk=str(self.uuid_codename))
            return __get_permission_name(self, instance)
    else:
        return self.content_type.model + ' | ' + self.name

Permission.add_to_class('uuid_codename', models.CharField(max_length=1000))
Permission._meta.get_field("codename")._unique = True
Permission._meta.get_field("name").max_length = 1000

Permission.__str__ = custom

Group.add_to_class('owner', models.ForeignKey(get_user_model()))

from utils import create_slug


def pre_save_create_slug(sender, instance, **kwargs):
    """
    Create slug value from object title.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    if not instance.slug:
        instance.slug = create_slug(sender, instance)

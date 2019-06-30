from .models import Consultation
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

@receiver(post_save, sender=Consultation)
def index_consultation(sender, instance, **kwargs):
    instance.indexing()

@receiver(pre_delete, sender=Consultation)
def delete_consultation(sender, instance, **kwargs):
    instance.delete()

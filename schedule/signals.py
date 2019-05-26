from .models import Consultation
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Consultation)
def index_consultation(sender, instance, **kwargs):
    instance.indexing()

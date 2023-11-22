from os import remove
from os.path import isfile

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import ShoesPhotoModel, JacketPhotoModel, TrouserPhotoModel, ThermalUnderwearPhotoModel, JumperPhotoModel

@receiver(post_delete, sender=ShoesPhotoModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo:
        if isfile(instance.photo.path):
            remove(instance.photo.path)

@receiver(pre_save, sender=ShoesPhotoModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_photo = ShoesPhotoModel.objects.get(pk=instance.pk).photo
    except ShoesPhotoModel.DoesNotExist:
        return False
    new_photo = instance.photo
    if old_photo != new_photo:
        if isfile(old_photo.path):
            remove(old_photo.path)

@receiver(post_delete, sender=JacketPhotoModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo:
        if isfile(instance.photo.path):
            remove(instance.photo.path)
# Куртка 
@receiver(pre_save, sender=JacketPhotoModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_photo = JacketPhotoModel.objects.get(pk=instance.pk).photo
    except JacketPhotoModel.DoesNotExist:
        return False
    new_photo = instance.photo
    if old_photo != new_photo:
        if isfile(old_photo.path):
            remove(old_photo.path)
# Джемпер 
@receiver(pre_save, sender= TrouserPhotoModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_photo =  TrouserPhotoModel.objects.get(pk=instance.pk).photo
    except  TrouserPhotoModel.DoesNotExist:
        return False
    new_photo = instance.photo
    if old_photo != new_photo:
        if isfile(old_photo.path):
            remove(old_photo.path)
# Термобелье
@receiver(pre_save, sender=ThermalUnderwearPhotoModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_photo = ThermalUnderwearPhotoModel.objects.get(pk=instance.pk).photo
    except ThermalUnderwearPhotoModel.DoesNotExist:
        return False
    new_photo = instance.photo
    if old_photo != new_photo:
        if isfile(old_photo.path):
            remove(old_photo.path)

@receiver(pre_save, sender=JumperPhotoModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_photo = JumperPhotoModel.objects.get(pk=instance.pk).photo
    except JumperPhotoModel.DoesNotExist:
        return False
    new_photo = instance.photo
    if old_photo != new_photo:
        if isfile(old_photo.path):
            remove(old_photo.path)



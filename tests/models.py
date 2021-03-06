# -*- encoding: utf-8 -*-

from __future__ import absolute_import

from django.db import models
from django_permanent.managers import MultiPassThroughManager
from django_permanent.models import PermanentModel
from django_permanent.query import DeletedQuerySet, PermanentQuerySet, NonDeletedQuerySet

from .cond import model_utils_installed


class BaseTestModel(models.Model):

    class Meta():
        abstract = True

    def __unicode__(self):
        return unicode(self.pk)


class MyPermanentModel(BaseTestModel, PermanentModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    pass


class RemovableDepended(BaseTestModel):
    dependance = models.ForeignKey(MyPermanentModel)


class NonRemovableDepended(BaseTestModel, PermanentModel):
    dependance = models.ForeignKey(MyPermanentModel, on_delete=models.DO_NOTHING)


class PermanentDepended(BaseTestModel, PermanentModel):
    dependance = models.ForeignKey(MyPermanentModel)


class MyPermanentQuerySet(PermanentQuerySet):
    def test(self):
        pass


class MyPermanentModelWithManager(BaseTestModel, PermanentModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    objects = MultiPassThroughManager(MyPermanentQuerySet, NonDeletedQuerySet)
    deleted_objects = MultiPassThroughManager(MyPermanentQuerySet, DeletedQuerySet)
    any_objects = MultiPassThroughManager(MyPermanentQuerySet, PermanentQuerySet)


if model_utils_installed:

    class TestQS(object):
        def test(self):
            return "ok"

    class CustomQsPermanent(BaseTestModel, PermanentModel):
        objects = MultiPassThroughManager(TestQS, DeletedQuerySet)

# -*- coding: utf-8 -*-
#
import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelMixin


class BaseAbstractSessionCommand(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.CharField(max_length=64, db_index=True, verbose_name=_("User"))
    input = models.CharField(max_length=128, db_index=True, verbose_name=_("Input"))
    output = models.CharField(max_length=1024, blank=True, verbose_name=_("Output"))
    session = models.CharField(max_length=36, db_index=True, verbose_name=_("Session"))
    timestamp = models.IntegerField(db_index=True)

    @classmethod
    def from_dict(cls, d):
        self = cls()
        for k, v in d.items():
            setattr(self, k, v)
        return self

    @classmethod
    def from_multi_dict(cls, l):
        commands = []
        for d in l:
            command = cls.from_dict(d)
            commands.append(command)
        return commands

    def to_dict(self):
        d = {}
        for field in self._meta.fields:
            d[field.name] = getattr(self, field.name)
        return d

    def __str__(self):
        return self.input

    class Meta:
        abstract = True


class AbstractSessionCommand(BaseAbstractSessionCommand):
    asset = models.CharField(max_length=128, db_index=True, verbose_name=_("Asset"))
    system_user = models.CharField(max_length=64, db_index=True, verbose_name=_("System user"))

    class Meta:
        abstract = True


class AbstractDatabaseSessionCommand(BaseAbstractSessionCommand):
    user_id = models.CharField(max_length=36, db_index=True, verbose_name=_("User ID"))
    database = models.CharField(max_length=128, verbose_name=_('Database'))
    database_id = models.CharField(max_length=36, db_index=True, verbose_name=_("Database ID"))
    db_host = models.CharField(max_length=128, verbose_name=_('Database host'))
    db_name = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Database name'))
    db_user = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('Database user'))

    class Meta:
        abstract = True


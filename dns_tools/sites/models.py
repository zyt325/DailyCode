from django.db import models


# Create your models here.

class DnsToolBindrr(models.Model):
    type = models.CharField(max_length=12, blank=True, null=True)
    domain_name = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=20, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    disabled_flag = models.IntegerField()
    reversed_flag = models.IntegerField()
    last_modified_date = models.DateTimeField()
    last_modified_user = models.CharField(max_length=40, blank=True, null=True)
    related_to_id = models.IntegerField(unique=True, blank=True, null=True)
    zone = models.ForeignKey('DnsToolBindzones', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return '%s %s %s %s' % (self.zone.zone_name, self.domain_name, self.type, self.value)

    class Meta:
        db_table = 'dns_tool_bindrr'
        unique_together = (('type', 'domain_name', 'value', 'zone'),)


class DnsToolBindzones(models.Model):
    zone_name = models.CharField(max_length=90, blank=True, null=True)
    serial_num = models.CharField(max_length=20, blank=True, null=True)
    start_part = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=3, blank=True, null=True)
    parent_to = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.zone_name, self.city)

    class Meta:
        db_table = 'dns_tool_bindzones'


class DnsRrs(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=12, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=3, blank=True, null=True)
    zone_name = models.CharField(max_length=90, blank=True, null=True)
    zone_id = models.IntegerField(blank=True, null=True)
    direction = models.CharField(max_length=10, blank=True, null=True)
    disabled_flag = models.IntegerField()
    reversed_flag = models.IntegerField()
    user = models.CharField(max_length=40, blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'dns_rrs'

    def toJSON1(self):
        import json

        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

    def toJSON(self):
        fields = []
        import datetime
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)
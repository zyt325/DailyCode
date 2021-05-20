from django import forms
from .models import DnsToolBindzones

query_city=DnsToolBindzones.objects.using("dns").filter(type='Forward').values('city').distinct()
CITY=[]
for c in query_city:
    CITY.append((c['city'],c['city']))
# query_zone=DnsToolBindzones.objects.filter(type='Forward').values('city','zone_name','parent_to').order_by('-parent_to')
query_zone=DnsToolBindzones.objects.using("dns").filter(type='Forward').values('city','zone_name','parent_to').order_by('parent_to')
ZONE={}
for i in query_zone:
    ZONE.setdefault(i['city'],[]).append((i['zone_name'],i['zone_name']))
CNAME=CITY

class addForm(forms.Form):
    name = forms.CharField(max_length=100,required=True)
    type = forms.ChoiceField(widget=forms.Select,choices=[('A','A'),('CNAME','CNAME')])
    value = forms.CharField(max_length=100,required=True)
    city = forms.ChoiceField(widget=forms.Select, choices=CITY)
    zone_name = forms.ChoiceField(widget=forms.Select, choices=ZONE)
    cname = forms.ChoiceField(widget=forms.CheckboxSelectMultiple,choices=CNAME)
    disabled_flag = forms.BooleanField(required=False)
    reversed_flag = forms.BooleanField(required=False)
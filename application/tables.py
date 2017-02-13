# -*- coding: utf-8 -*-
import django_tables2 as tables
from application.models import vrijeme_promet, Requests_vrijeme, Status, Najaktivniji, Contents, ipcontent
from table import Table
from table.columns import Column
from django_tables2.utils import A

class SimpleTable(tables.Table):
    class Meta:
        model = Najaktivniji
        exclude = ('id', )
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}


class searchtable(Table):    
    ip = Column(field='ip', header='ip')
    brojponavljanja = Column(field='brojponavljanja', header='brojponavljanja') 
    class Meta:
        model = Najaktivniji
        attrs = {'class': 'custom_class'}


class secundsearch(Table):    
    content = Column(field='content', header='content')
    brojponavljanja = Column(field='brojponavljanja', header='brojponavljanja') 
    class Meta:
        model = Contents
        attrs = {'class': 'moja_clasa'}

class trecisearch(Table):
    vrijeme = Column(field='vrijeme', header='vrijeme')
    requests = Column(field='requests', header='requests')

    class Meta:
        model =  Requests_vrijeme
        attrs = {'class': 'moja_treca'}

'''
class cetvrtisearch(Table):    
    ip = Column(field='ip', header='ip')
    content = Column(field='content', header='content')
    counts = Column(field='counts', header='counts')  
    class Meta:
        model = ipcontent
        per_page = 50
        attrs = {'class': 'moja_cetvrta'}

'''

class cetvrtisearch(tables.Table):
    class Meta:
        model = ipcontent
        exclude = ('id', )
        attrs = {'class': 'paleblue'}

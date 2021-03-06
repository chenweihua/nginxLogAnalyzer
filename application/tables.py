# -*- coding: utf-8 -*-
import django_tables2 as tables
from application.models import vrijeme_promet, Requests_vrijeme, Status, Najaktivniji, Contents, ipcontent
from table import Table
from table.columns import Column
from django_tables2.utils import A

'''
    This tables.py provide search or pagination for django tables, 
    in this class we define field that will be search field or we 
    define pagination per specific django tables!

'''

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

class cetvrtisearch(tables.Table):
    class Meta:
        model = ipcontent
        exclude = ('id', )
        attrs = {'class': 'paleblue'}

class searchtable2(tables.Table):
    class Meta:
        model = Contents
        exclude = ('id', )
        attrs = {'class': 'paleblue'}

class searchtable3(tables.Table):
    class Meta:
        model = Requests_vrijeme
        exclude = ('id', )
        attrs = {'class': 'paleblue'}
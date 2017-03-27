#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from application.models import nginxLog, overall, regex, vrijeme_promet, ipcontent, Requests_vrijeme, Status, Najaktivniji, Contents, Document, status_per_hour206, status_per_hour200, status_per_hour404, status_per_hour301, status_per_hour302, status_per_hour403, status_per_hour405, status_per_hour406, status_per_hour500, status_per_hour504
from application.serializers import VrijemePrometSerializer, IpcontentSerializer, RequestSerializer, StatusSerializer, NajaktivnijiSerializer, ContentSerializer, CodeSerializer200, CodeSerializer206, CodeSerializer404, CodeSerializer301, CodeSerializer302, CodeSerializer403, CodeSerializer405, CodeSerializer406, CodeSerializer500, CodeSerializer504
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import json
import os
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django_tables2 import RequestConfig
from .tables import searchtable, SimpleTable, searchtable2, searchtable3, secundsearch, trecisearch, cetvrtisearch
from .forms import DocumentForm
import subprocess
import psycopg2
from wsgiref.util import FileWrapper
import mimetypes
from django.contrib.auth.decorators import login_required
import glob
import re
from django.db.models import Sum
import commands
import socket
#from django.views.generic import ListView
#from braces.views import LoginRequiredMixin, GroupRequiredMixin
#from django.template import RequestContext
#from django.shortcuts import get_object_or_404, redirect
#from django.template.response import TemplateResponse
#from django.core.paginator import Paginator
#from decimal import Decimal, ROUND_HALF_UP


'''
    Make data for REST API - get all data from table "vrijeme_promet_variable", and make serializeration 
    for REST API calling VrijemePrometSerializer!
    The REST API can be called using name of this class "SnippetList", for example:
    if we read urls.py file, we can find this line "url(r'^application/$', views.SnippetList.as_view())",
    that means for example "http:localhost/application" on that URL you can se your Django REST API that return 
    json file,this REST API will use D3.js for making graph!
'''
BASE_DIR = os.getcwd()
class SnippetList(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        vrijeme_promet_variable = vrijeme_promet.objects.all()
        serializer = VrijemePrometSerializer(vrijeme_promet_variable, many=True)
        return Response(serializer.data)

'''
    Make data for REST API - get all data from table "ipcontent", and make serializeration for REST API 
    calling IpcontentSerializer! The REST API can be called using name of this class "Ipcontenlist", for example:
    if we read urls.py file, we can find this line "url(r'^ipcontent/$', views.Ipcontenlist.as_view()),",
    that means for example "http:localhost/ipcontent" on that URL you can se your Django REST API that return json file 
    this REST API will use Django tables for making HTML tables!
'''
class Ipcontenlist(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        ipcontentt = ipcontent.objects.all().filter().order_by('-ip')
        serializer = IpcontentSerializer(ipcontentt, many=True)
        return Response(serializer.data)

'''
    Make data for REST API - get all data from tables "status_per_hour200, status_per_hour206, status_per_hour404", and make serializeration for REST API 
    calling serializer200, serializer206, serializer404! The REST API can be called using name of this class "CodeList", for example:
    if we read urls.py file, we can find this line "url(r'^code/$', views.CodeList.as_view()),",
    that means for example "http:localhost/CodeList" on that URL you can se your Django REST API that return json file 
    this REST API will use D3.js for making graph!
'''
class CodeList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        code200 = status_per_hour200.objects.all()
        code206 = status_per_hour206.objects.all()
        code404 = status_per_hour404.objects.all()
        serializer200 = CodeSerializer200(code200, many=True)
        serializer206 = CodeSerializer206(code206, many=True)
        serializer404 = CodeSerializer404(code404, many=True)
        return Response([serializer200.data] + [serializer206.data] + [serializer404.data])


# This is also for making Django REST API!

class CodeList200(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        code200 = status_per_hour200.objects.values('time', 'y')     
        serializer200 = CodeSerializer200(code200, many=True)       

        return Response(serializer200.data)

class CodeList404(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):        
       
        code404 = status_per_hour404.objects.values('time', 'y')      
        serializer404 = CodeSerializer404(code404, many=True)
        return Response(serializer404.data)

class CodeList206(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):      
        code206 = status_per_hour206.objects.values('time', 'y')       
        serializer206 = CodeSerializer206(code206, many=True)        
        return Response(serializer206.data)

class CodeList301(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):      
        code301 = status_per_hour301.objects.values('time', 'y')       
        serializer301 = CodeSerializer301(code301, many=True)        
        return Response(serializer301.data)

class CodeList302(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):      
        code302 = status_per_hour302.objects.values('time', 'y')       
        serializer302 = CodeSerializer302(code302, many=True)        
        return Response(serializer302.data)

class CodeList403(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):      
        code403 = status_per_hour403.objects.values('time', 'y')       
        serializer403 = CodeSerializer403(code403, many=True)        
        return Response(serializer403.data)

class CodeList405(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):      
        code405 = status_per_hour405.objects.values('time', 'y')       
        serializer405 = CodeSerializer405(code405, many=True)        
        return Response(serializer405.data)

class CodeList406(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):      
        code406 = status_per_hour406.objects.values('time', 'y')       
        serializer406 = CodeSerializer406(code406, many=True)        
        return Response(serializer406.data)

class CodeList500(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):      
        code500 = status_per_hour500.objects.values('time', 'y')       
        serializer500 = CodeSerializer500(code500, many=True)        
        return Response(serializer500.data)

class CodeList504(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):      
        code504 = status_per_hour504.objects.values('time', 'y')       
        serializer504 = CodeSerializer504(code504, many=True)        
        return Response(serializer504.data)

class RequestList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        requests = Requests_vrijeme.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return json.dumps(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusList(APIView):

    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        ukupno = Status.objects.aggregate(Sum('brojponavljanja'))
        status = Status.objects.all()
        
        serializer = StatusSerializer(status, many=True)
        
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return json.dumps(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NajaktivnijiList(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        ip = Najaktivniji.objects.select_related().all()
        serializer = NajaktivnijiSerializer(ip, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NajaktivnijiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return json.dumps(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentList(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, format=None):

        content = Contents.objects.select_related().all().filter().order_by('-brojponavljanja')
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return json.dumps(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListaTemplate(TemplateView):

    template_name = 'app/sadrzaj.html'
    def get_content(self, **kwargs):
        context = super(ListaTemplate, self).get_context_data(**kwargs)
        context['contents_list'] = Contents.objects.all()
        return context

    def get_ip(self, **kwargs):
        context = super(ListaTemplate, self).get_context_data(**kwargs)
        context['ip_list'] = Najaktivniji.objects.all()
        return context

    def get_status(self, **kwargs):
        context = super(ListaTemplate, self).get_context_data(**kwargs)
        context['status_list'] = Status.objects.all()
        return context

    def get_requests(self, **kwargs):
        context = super(ListaTemplate, self).get_context_data(**kwargs)
        context['requests_list'] = Requests_vrijeme.objects.all()
        return context
'''
    This function make django tables, if you read this line 'url(r'^table/$', views.dataTabs, name="table"),'
    from urls.py, you can see that table can be called  for example on this URL http:localhost/table
    in this function we use pagination if we have large data in tables, if not we make django search table instead 
    this pagination django tables, this is useful because we don't want to break our application with large so we use pagination!
'''
def dataTabs(request):
    queryset = Najaktivniji.objects.all()
    rows = Najaktivniji.objects.count()

    print type(rows)
    if rows > 2000:
        postdata = SimpleTable(queryset)
        RequestConfig(request, paginate={"per_page": 20}).configure(postdata)
        return render(request, "app/tablePrim.html", {'postdata': postdata})
    else:
        postdata = searchtable(queryset)
        return render(request, "app/table.html", {'postdata': postdata})

# This is same as above, make django table function with pagination - 20 rows per page!

def datacontent(request):

    queryset = Contents.objects.all()
    rows = Contents.objects.count()

    print type(rows)
    if rows > 2000:
        fajlovi = searchtable2(queryset)
        RequestConfig(request, paginate={"per_page": 20}).configure(fajlovi)
        return render(request, "app/table2Prim.html", {'fajlovi': fajlovi})
    else:
        fajlovi = secundsearch(queryset)
        return render(request, "app/table2.html", {'fajlovi': fajlovi})


def vrijemeview(request):

    queryset = Requests_vrijeme.objects.all()
    rows = Requests_vrijeme.objects.count()

    print type(rows)
    if rows > 2000:
        vrijemerequest = searchtable3(queryset)
        RequestConfig(request, paginate={"per_page": 20}).configure(vrijemerequest)
        return render(request, "app/table3Prim.html", {'vrijemerequest': vrijemerequest})
    else:
        vrijemerequest = trecisearch(queryset)
        return render(request, "app/table3.html", {'vrijemerequest': vrijemerequest})



def simple_list(request):
    queryset = ipcontent.objects.all()
    ipcontentrequest = cetvrtisearch(queryset)
    RequestConfig(request, paginate={"per_page": 30}).configure(ipcontentrequest)

    return render(request, 'app/table4.html', {'ipcontentrequest': ipcontentrequest})

# This @login_required means only registred user can call this function 
# This function uplaod user log file, and return on frontend name of uploaded log files    
@login_required
def procesing_html(request):

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()        
            return HttpResponseRedirect(reverse('upload'))
        else:            
            return HttpResponse("Please chose your file for upload!!!")
    else:
        form = DocumentForm()
        documents = Document.objects.all()
        print documents
    return render(request, 'app/upload.html', {'documents': documents, 'form': form})

'''
    This function allow user to delete uploaded log file, before run analyzer, this is useful when user upload wrong file
    and want to upload another file before run log analyzer!
'''
def delete(request, stb_id=None):
    print stb_id
    if Document.objects.filter(id=stb_id).exists():
        stb = Document.objects.get(id=stb_id)
        stb.delete()
        return HttpResponseRedirect(reverse('upload'))
# This function make js search table file, and this files user can download locally! 
try:
    conn = psycopg2.connect("dbname='nginxbase' user='nginx' host='localhost' password='789ivanino'")
except:
    print "I am unable to connect to the database"
def html_tablica(tablica):
    file = tablica + str('.html')

    cursor4 = conn.cursor('cursor4')
    cursor4.execute("SELECT * FROM " + str(tablica))
    outfile = open(file, "w")
    tmp = cursor4.fetchall()
    col_names = []
    for elt in cursor4.description:
        col_names.append(elt[0])

    print >> outfile, """<html>
    <head>
    <style>
    #myInput {
      background-image: url('/css/searchicon.png');
      background-position: 10px 10px;
      background-repeat: no-repeat;
      width: 50%;
      font-size: 16px;
      padding: 12px 20px 12px 40px;
      border: 1px solid #ddd;
      margin-bottom: 12px;
    }
    table, th, td {
      width: 50%;
      border-collapse: separate;
      font: 14px/1.4 "Helvetica Neue", Helvetica, Arial, sans-serif;
      border: 1px solid black;
    }
    th, td {
      padding: 10px 15px;
      vertical-align: middle;
    }
    #myheader {
      background: #395870;
      background: linear-gradient(#49708f, #293f50);
      color: #fff;
      font-size: 11px;
      text-transform: uppercase;
      padding: 10px 15px;
      vertical-align: middle;
    }
    #mytdbody{

      background: linear-gradient(#8080ff, #293f50);
      color: #fff;
      font-size: 11px;
      padding: 2px;
      text-align: center;
      font-size:8pt;
    }
    thead {
      background: #395870;
      background: linear-gradient(#49708f, #293f50);
      color: #fff;
      font-size: 11px;
      text-transform: uppercase;
    }
    </style>
    </head>
    <body>
    <section class="container">

    <h2>Light Javascript Table Filter</h2>

    <input id="myInput" type="search" class="light-table-filter" data-table="order-table" placeholder="Filter ...">

    <table class="order-table table" id="myTable">"""
    print >>outfile, "<thead> <tr><th>%s</th><th>%s</th></tr></thead>" % (col_names[1], col_names[2])

    print >>outfile, """<tbody id="mytdbody">"""
    for elementi in tmp:
        print >>outfile, "<tr><td>%s</td><td>%s</td></tr>" % (elementi[1], elementi[2])
    print >>outfile, """</tbody>
    </table>
    </section>
    <script type="text/javascript">
    (function(document) {
    'use strict';

    var LightTableFilter = (function(Arr) {

    var _input;

    function _onInputEvent(e) {
      _input = e.target;
      var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
      Arr.forEach.call(tables, function(table) {
        Arr.forEach.call(table.tBodies, function(tbody) {
          Arr.forEach.call(tbody.rows, _filter);
        });
      });
    }

    function _filter(row) {
      var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
      row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
    }

    return {
      init: function() {
        var inputs = document.getElementsByClassName('light-table-filter');
        Arr.forEach.call(inputs, function(input) {
          input.oninput = _onInputEvent;
        });
      }
    };
    })(Array.prototype);

    document.addEventListener('readystatechange', function() {
    if (document.readyState === 'complete') {
      LightTableFilter.init();
    }
    });

    })(document);
    </script>
    """

    '''
    dio koji iscrtava html tablicu preko html modula
    HTMLFILE = 'HTML_tutorial_output.html'
    f = open(HTMLFILE, 'w')
    htmlcode = HTML.table(cursor4, header_row=['Promet', 'Vrijeme'], col_align = 'center', col_styles = 'background-color:blue;')
    print htmlcode
    f.write(htmlcode)
    f.write('<p>')
    print '-'*79
    '''
    conn.commit()
    outfile.close()

@login_required
def run_script(request):
    if (request.POST.get('tablice')):       
        overall.objects.all().delete()
        regex.objects.all().delete()
        vrijeme_promet.objects.all().delete()
        ipcontent.objects.all().delete()
        Requests_vrijeme.objects.all().delete()
        Status.objects.all().delete()
        Najaktivniji.objects.all().delete()
        Contents.objects.all().delete()
        Document.objects.all().delete()
        status_per_hour206.objects.all().delete()
        status_per_hour200.objects.all().delete()
        status_per_hour404.objects.all().delete()
        status_per_hour301.objects.all().delete()
        status_per_hour302.objects.all().delete()
        status_per_hour403.objects.all().delete()
        status_per_hour405.objects.all().delete()
        status_per_hour406.objects.all().delete()
        status_per_hour500.objects.all().delete()
        status_per_hour504.objects.all().delete()
    if (request.POST.get('mybtn')):

        proc = subprocess.Popen(["if [[ $(ps aux | grep main_script.py | grep -vc grep)  > 0 ]]; then echo 1; else echo 0 ; fi"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        var = int(out)
        if var == 0:
            print "Your analyzer is activated!"
            # Your log analyzer is activated!
            nginxLog.objects.all().delete()
                    
            lista = glob.glob(BASE_DIR+str('*.html'))
            for name in lista:
                if os.path.isfile(name):
                    print name
                    html_tables_dir = len(BASE_DIR)
                    y = name[html_tables_dir:]
                    print y
                    files = open(y, "w")
                    files.close()                        
                    os.remove(name)
       
            os.system("python main_script.py")
            html_tablica('application_najaktivniji')
            html_tablica('application_vrijeme_promet')
            html_tablica('application_status')
            html_tablica('application_requests_vrijeme')
            html_tablica('application_contents')
      
        else:           
            return HttpResponse("Your log analyzer is already activated, please wait !!")

    check_html = subprocess.Popen(["if [[ $(ls | grep 'application_contents.html' )  == 'application_contents.html' ]]; then echo 1; else echo 0 ; fi"], stdout=subprocess.PIPE, shell=True)
    (check_html, err) = check_html.communicate()
    bash_test = int(check_html)

    # In this block of code, we check which html table user are clicked for download!
    if (request.POST.get('download1')):
        if bash_test == 1:
            print 'download1'
            filename = BASE_DIR+str('/application_contents.html')
            download_name = "application_contents.html"
            wrapper = FileWrapper(open(filename))
            content_type = mimetypes.guess_type(filename)[0]
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = "attachment; filename=%s" % download_name
            return response
        else:
           
            return HttpResponse("HTML tables are not generated !!!")

    elif (request.POST.get('download2')):
        if bash_test == 1:
            filename = BASE_DIR+str('/application_najaktivniji.html')
            download_name = "application_najaktivniji.html"
            print 'download2'
            wrapper = FileWrapper(open(filename))
            content_type = mimetypes.guess_type(filename)[0]
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = "attachment; filename=%s" % download_name
            return response
        else:
            
            return HttpResponse("HTML tables are not generated !!!")

    elif (request.POST.get('download3')):
        if bash_test == 1:

            filename = BASE_DIR+str('/application_requests_vrijeme.html')
            download_name = "application_requests_vrijeme.html"
            print 'download3'
            wrapper = FileWrapper(open(filename))
            content_type = mimetypes.guess_type(filename)[0]
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = "attachment; filename=%s" % download_name
            return response
        else:
            return HttpResponse("HTML tables are not generated !!!")


    elif (request.POST.get('download4')):
        if bash_test == 1:

            filename = BASE_DIR+str('/application_vrijeme_promet.html')
            download_name = "application_vrijeme_promet.html"
            print 'download4'
            wrapper = FileWrapper(open(filename))
            content_type = mimetypes.guess_type(filename)[0]
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = "attachment; filename=%s" % download_name
            return response
        else:
            return HttpResponse("HTML tables are not generated!!!")

    elif (request.POST.get('download5')):
        if bash_test == 1:

            filename = BASE_DIR+str('/application_status.html')
            download_name = "application_status.html"
            print 'download5'
            wrapper = FileWrapper(open(filename))
            content_type = mimetypes.guess_type(filename)[0]
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = "attachment; filename=%s" % download_name
            return response
        else:
            return HttpResponse("HTML tables are not generated !!!")
    return render(request, 'app/procesing.html')

# This function serve overall data on frontend page!
@login_required
def nginx_graphOne(request):

    queryset = overall.objects.all().values('promet', 'code200', 'code404', 'ip', 'content', 'fajl', 'code', 'total', 'metod', 'status400', 'status403', 'scripttime')
     
    for myDict in queryset:
        for k, v in myDict.items():
            if v == None:
                del myDict[k]
    
    seen = set()
    querysett = []
    for d in queryset:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            querysett.append(d)

    return render(request, 'app/nginxgraph1.html', {'querysett': querysett})

''' This function serve data for draw graphs and django tables.'''
@login_required
def nginx_graphTwo(request):
    return render_to_response('app/nginxgraph2.html')

@login_required
def nginx_graphtreci(request):
    return render_to_response('app/nginxgraph3.html')

@login_required
def nginx_cetvrti(request):
    return render_to_response('app/nginxgraph4.html')

@login_required
def graph(request):
    return render_to_response('app/graph1.html')

@login_required(login_url="login/")
def home(request):
    return render(request,"home.html")

def static(request):
   return render_to_response('app/index.html')

def static1(request):    
   return render_to_response('app/overall.html')

'''
This function catch regex from user via frontend  form, and make validation for this regex
if regex match desired field and desired format this regex will be stored in the databse
and this regex will be used in this curent iteration!
'''

def searchregwx(request):
    varreturn = []
 
    if request.method == "POST":
        regext = request.POST['regex1']
        string = request.POST['regex2']
        prog = re.compile(regext)
        match = prog.search(string)
        if match:
            f = open( 'custom_regex.txt', 'w' )
            f.write( regext )
            f.close()
            var = 'found', match.group()
            varreturn.append(var)
            t = regex(id=1, regex = regext, status ='not done')
            t.save()
            #p = regex(regex=regext)

        else:      
            var1 =  'did not', 'find'
            varreturn.append(var1)

    return render(request, 'app/regex.html', {'varreturn':varreturn})
      
def defaultempty(request):    
   return render_to_response('app/defaultempty.html')

def default2(request):    
   return render_to_response('app/default2.html')

# This function catch data from user (desired number of request per client that will be used once)!
def total_client_request_defined_by_user(request): 
 
    if request.method == "POST":
        string1 = request.POST['string1']
        print string1
        x = overall(id=1, userdefineminimalrequest = string1)
        x.save()

    return render(request, 'app/userclient.html')

''' 
    This function chatch data from user, and make validation if this data is IP address,
    and after that Whois function return on frontend information about that IP address, using linux "whois" command!
'''
def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def Whois(request):
    
    result = []
    if request.method == "POST":
        string1 = request.POST['string1']
        print string1
        ip = is_valid_ipv4_address(string1)

        if ip == True:
            command = 'whois '+str(string1)
            output = commands.getstatusoutput(command)
            for i in output:
                print i
                result.append(i)
        else:          
            result = 'Not valid IP'           

    return render(request, 'app/whois.html', {'result':result})


   


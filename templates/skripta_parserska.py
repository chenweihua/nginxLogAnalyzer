#!/usr/bin/nginx_log_analyzer_env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import re
import psycopg2
import multiprocessing as mp
from decimal import Decimal, ROUND_HALF_UP
import subprocess
import glob
import zipfile
import os.path
import subprocess
import sys
import csv
import datetime


def logProces():
    try:
        fileexts = ['.tar.gz', '.gz', '.zip']
        check = subprocess.Popen(["if [[ $(ls -1 /home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload | wc -l)  > 1 ]]; then echo 1; else echo 0 ; fi"], stdout=subprocess.PIPE, shell=True)
        (out, err) = check.communicate()
        var = int(out)

        if var == 1:
            print "Fajlova ima vise od jednog!"
            lista = glob.glob('/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/*')            
            for name in lista:
                try:
                    for ext in fileexts:
                        if name.endswith(ext):                           
                            if ext == '.zip':             
                                y = name[63:]                                             
                                filename = '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/'+str(y)
                                subprocess.call(['unzip', '-j', '-o', filename, '-d', '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload']) 
                                os.remove(filename)
                            elif ext == '.tar.gz':
                                z = name[63:]               
                                filenamez = '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/'+str(z)
                                subprocess.call(['tar', '-zxvf', filenamez, '-C', '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload']) 
                                os.remove(filenamez)
                            elif ext == '.gz':
                                c = name[63:]               
                                filenamez = '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/'+str(c)
                                subprocess.call(['gunzip', filenamez])                                
                            else:
                                print "Predane extenzije nisu podržane!"
                                sys.exit()                
                except:
                    print 'unzip error'        
            lista2 = glob.glob('/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/*') 
            
            for unzipani in lista2:
                x = unzipani[63:]            
                filepath = '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/'+str(x)
                os.rename(filepath, filepath.replace(" ", "_"))
            final_list = []  
            lista3 = glob.glob('/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/*')
            for files in lista3:
                final_list.append(files)                 
         
            with open("access.log", "wb") as outfile:
                for f in final_list:
                    with open(f, "rb") as infile:
                        outfile.write("\n"+ infile.read())
            lista4 = glob.glob('/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/*')
            for files4 in lista4:
                os.remove(files4)
        else:
            try:
                print "Fajlova ima 0 ili 1"
                filelog = glob.glob('/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/*')
                for logs in filelog:
             
                    for exty in fileexts:
                        if logs.endswith(exty):                           
                            if exty == '.zip':
                                subprocess.call(['unzip', '-j', '-o', logs, '-d', '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload'])
                                os.remove(logs)
                                
                            elif exty == '.tar.gz':                
                     
                                subprocess.call(['tar', '-zxvf', logs, '-C', '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload'])                        
                                os.remove(logs)
                            elif exty == '.gz':                
                     
                                subprocess.call(['gunzip', logs])                        
                                                                                 
                            else:
                                print "Predane extenzije nisu podržane!"
                                sys.exit()
                filelogTar1 = glob.glob('/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/*')
                for itemOne in filelogTar1:
                    p = itemOne[63:]
                    old_f = '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/upload/'+str(p)
                    new_f = '/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/access.log'               
                    os.rename(old_f,new_f)
            except:
                print "else statement error"
    except:
        print "F-ja logProces error!"               

#logProces()

danasnji_log = "access.log"
try:
    conn = psycopg2.connect("dbname='nginxbase' user='nginx' host='localhost' password='789ivanino'")
except:
    print "I am unable to connect to the database"

def brisem(tablica):
    cursor_delete = conn.cursor()
    truncate = """truncate table """ + str(tablica) +str(' RESTART IDENTITY;') 
    cursor_delete.execute(truncate)
    conn.commit()
'''
# multiprocesing multithreading parse access.log
os.system("rm -rf /tmp/mycsvfile.csv")
os.system("touch /tmp/mycsvfile.csv")
def process_wrapper(chunkStart, chunkSize):
    
    pattern = re.compile(r'^([0-9.]+)\s-\s-\s\[(.+)\]\s"([a-zA-Z]+)\s(.+)\s\w+/.+\s([0-9.]+)\s([0-9.]+)\s"(.+)"\s"(.+)"')
    csvfile = '/tmp/mycsvfile.csv'
    f = open(csvfile, 'a')
    
    try:
        writer = csv.writer(f, delimiter=';')
        with open(danasnji_log) as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).splitlines()
            for line in lines:
                for m in re.finditer(pattern, line):                   
                    ip =        m.group(1)
                    vrijeme =   m.group(2)                               
                    request =   m.group(4)
                    status =    m.group(5)
                    bandwidth = m.group(6)                    
                    referrer =  m.group(7)
                    user_agent =  m.group(8)                 
                    writer.writerow( (ip, vrijeme, request, status, bandwidth, user_agent, referrer) )     
    finally:
        f.close()
            
def chunkify(fname, size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname, 'r') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size, 1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

pool = mp.Pool(1)
jobs = []


for chunkStart, chunkSize in chunkify(danasnji_log):
    jobs.append(pool.apply_async(process_wrapper, (chunkStart, chunkSize)))
for job in jobs:
    job.get()
pool.close()

print 'sada brisem tablicu'
brisem('application_nginxlog')
cur = conn.cursor()
print 'obriso sam, sada radim select procesing'
cur.execute("SELECT * FROM function_csv();")
cur.close()
conn.commit()


# F-ja kolicina prometa u jedinici vremena 
def promet_vrijeme():
    print "F-ja: promet_vrijeme"
    brisem('application_vrijeme_promet')
    cursor2 = conn.cursor('cursor2')
    cursor2.itersize = 100000
    cursor2.execute("SELECT bandwidth, vrijeme FROM application_nginxlog")
    cptLigne = 0
    vrijeme_promet = {}
    dict_list = []

    for rec in cursor2:
        cptLigne += 1
        time = rec[1].strftime('%Y-%b-%d %H:%M')
        promet = rec[0]
        dicts = {'vrijeme': time, 'promet': promet}
        dict_list.append(dicts)
        # print 'punim dict_list' +str(cptLigne)        
        if cptLigne % 100000 == 0:
            print '% 100000 == 0' + str(cptLigne)
            for item in dict_list:
                vrijeme_promet[item['vrijeme']] = 0
                
            for item in dict_list:
                vrijeme_promet[item['vrijeme']] += item['promet']
                

            for key, values in sorted(vrijeme_promet.items()):
                cptLigne += 1
                vrijeme = key
                promet = values
                cursor3 = conn.cursor()
                
                query = "INSERT INTO application_vrijeme_promet(vrijeme, promet) VALUES (%s, %s);"
                data = (vrijeme, promet)
                cursor3.execute(query, data)
            
            vrijeme_promet = None
            dict_list = None
            vrijeme_promet = {}
            dict_list = []
    conn.commit()

    # sređivam duplo vrijeme iz baze snipet
    cursor4 = conn.cursor('cursor4')
    snipet_promet = {}
    snipet_lista = []
    cursor4.execute("SELECT promet, vrijeme FROM application_vrijeme_promet")
    for rec in cursor4:
        promet = rec[0]
        vrijeme = rec[1]
        dicts = {'vrijeme': vrijeme, 'promet': promet}
        snipet_lista.append(dicts)
    conn.commit()

    for record in snipet_lista:
        snipet_promet[record['vrijeme']] = 0
    for record in snipet_lista:
        snipet_promet[record['vrijeme']] += record['promet']

    brisem('application_vrijeme_promet')
    for key, values in sorted(snipet_promet.items()):
        cursor6 = conn.cursor()
        vrijeme = key
        promet_bayte = int(values)
        our_value = Decimal(promet_bayte/1048576)
        promet = Decimal(our_value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        # print 'dio kad spremam u bazu' +str(cptLigne)
        query = "INSERT INTO application_vrijeme_promet(vrijeme, promet) VALUES (%s, %s);"
        data = (vrijeme, promet)
        cursor6.execute(query, data)
    conn.commit()
promet_vrijeme()

# F-ja broj requesta u jedinici vremena
def request_vrijeme():
    print "F-ja: request_vrijeme"
    brisem('application_requests_vrijeme')
    cursor7 = conn.cursor('cursor7')
    cursor7.itersize = 100000
    cursor7.execute("SELECT vrijeme FROM application_nginxlog")
    cptLigne = 0
    lista_dictionaries = []
    request = {}
    for rec in cursor7:
        cptLigne += 1
        time = rec[0].strftime('%Y-%b-%d %H:%M')
        dictionary = {'vrijeme': time}
        lista_dictionaries.append(dictionary)
        if cptLigne % 100000 == 0:            
            for dic in lista_dictionaries:
                values = dic['vrijeme']
                request[values] = request.get(values, 0)+1
            for key, values in sorted(request.items()):
                vrijeme = key
                requests = values
                cursor8 = conn.cursor()
                query = "INSERT INTO application_requests_vrijeme(vrijeme, requests) VALUES (%s, %s);"
                data = (vrijeme, requests)
                cursor8.execute(query, data)
            request = None
            lista_dictionaries = None
            lista_dictionaries = []
            request = {}
    conn.commit()

    cursor9 = conn.cursor('cursor7')
    cursor9.execute("SELECT vrijeme, requests FROM application_requests_vrijeme")

    vrijeme_requestt = []
    vrijeme_req = {}

    for items in cursor9:
        vrijeme = items[0]
        requesti = items[1]
        dicts = {'vrijeme': vrijeme, 'requests': requesti}
        vrijeme_requestt.append(dicts)

    for item in vrijeme_requestt:
        vrijeme_req[item['vrijeme']] = 0

    for item in vrijeme_requestt:
        vrijeme_req[item['vrijeme']] += item['requests']
    conn.commit()
    brisem('application_requests_vrijeme')
    for vrijeme, requests in sorted(vrijeme_req.items()):
        cursor11 = conn.cursor()
        query = "INSERT INTO application_requests_vrijeme(vrijeme, requests) VALUES (%s, %s);"
        data = (vrijeme, requests)
        cursor11.execute(query, data)
    conn.commit()
request_vrijeme()


# F-ja koliko koji IP generira requesta, prikazujem samo ako je broj requesta po IPu veci od 500
def najaktivniji_IP():
    print "F-ja: najaktivniji_IP"
    brisem('application_najaktivniji')
    cursor_ip = conn.cursor('cursor_ip')
    cursor_ip.execute("SELECT ip, count(*) FROM application_nginxlog GROUP BY ip")   
    for item in cursor_ip:
        ip = item[0]
        brojponavljanja = item[1]
        if brojponavljanja >= 300:
            cursor_stat = conn.cursor()
            query = "INSERT INTO application_najaktivniji(ip, brojponavljanja) VALUES (%s, %s);"
            data = (ip, brojponavljanja)
            cursor_stat.execute(query, data)
    conn.commit()
najaktivniji_IP()


# F-ja koja prikazuje content po koji IP-ovi idu, s tim da prikazuje samo one contente ako je broj potrazvanja za contentom veci od 300
def get_content():
    print "F-ja: get_content"
    brisem('application_contents')
    cursor_ip = conn.cursor('statuss')
    cursor_ip.execute("SELECT request, count(*) FROM application_nginxlog GROUP BY request")
    for item in cursor_ip:
        content = item[0]
        brojponavljanja = item[1]
        cursor_stat = conn.cursor()
        if brojponavljanja >= 300:
            query = "INSERT INTO application_contents(content, brojponavljanja) VALUES (%s, %s);"
            data = (content, brojponavljanja)
            cursor_stat.execute(query, data)
    conn.commit()
get_content()


# F-ja broj requsta po status kodovima
def access_by_Response_code():
    print "F-ja: access_by_Response_code"
    brisem('application_status')
    cursor_response = conn.cursor('cursor_response')
    cursor_response.execute("SELECT status, count(*) FROM application_nginxlog GROUP BY status")
    for statusi in cursor_response:
        status = statusi[0]
        brojponavljanja = statusi[1]
        cursor_insert = conn.cursor()
        query = "INSERT INTO application_status(status, brojponavljanja) VALUES (%s, %s);"
        data = (status, brojponavljanja)
        cursor_insert.execute(query, data)
    conn.commit()
access_by_Response_code()

'''
# F-ja koja racuna broj 200, 404, 206 requesta u jedinici vremena
def status_per_hour(code):

    tablica = "application_status_per_hour"+str(code)+str('(time, y) VALUES (%s, %s);')
    delete_table = "application_status_per_hour"+str(code)
    brisem(delete_table)
    statushour = conn.cursor('statushour')
    select = "SELECT status, count(*), to_char(vrijeme, 'HH24') from application_nginxlog where status = '%s' GROUP BY to_char, status;"%str(code)
    statushour.execute(select) 
 
    lista1 = []
    lista2 = []
    lista  = ['00','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
 
    for x in statushour:
        time = x[2]     
        ponavljanje = x[1]
        dodati = time, ponavljanje
        lista2.append(dodati)
        lista1.append(time)
    
    for item in lista:
        if item not in lista1:
            dodati = item, 0
            lista2.append(dodati)
    lista2.sort()
    cursor_hour2 = conn.cursor()
    
    for items in lista2:
        time = items[0]
        y = items[1]
       
        insert = "INSERT INTO " +str(tablica)
        data = (time, y)
        cursor_hour2.execute(insert, data)
    print tablica

    conn.commit()

status_per_hour(200)
status_per_hour(206)
status_per_hour(301)
status_per_hour(302)
status_per_hour(403)
status_per_hour(404)
status_per_hour(405)
status_per_hour(406)
status_per_hour(500)
status_per_hour(504)
brisem('application_document')
 
def brisemStariLog():
    try:          
        name ='/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/access.log'
        if os.path.isfile(name):
            print name         
            y = name[56:]
            print y
            files = open(y, "w")
            files.close()                        
            os.remove(name)
    except:
        print "Brisanje log file-a!"

#brisemStariLog()
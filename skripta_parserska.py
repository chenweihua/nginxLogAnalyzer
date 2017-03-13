#!/usr/bin/nginx_log_analyzer_env python
# -*- coding: utf-8 -*-


from __future__ import division
import os
import re
import psycopg2
import multiprocessing as mp
#from decimal import Decimal, ROUND_HALF_UP
import subprocess
import glob
#import zipfile
import os.path
#import subprocess
import sys
import csv
#import datetime
#import copy
from psycopg2.extensions import AsIs
import time
start_time = time.time()
#from math import trunc
import traceback
import logging



try:
    conn = psycopg2.connect("dbname='nginxbase' user='nginx' host='localhost' password='789ivanino'")
except:
    print "I am unable to connect to the database"
danasnji_log = "access.log"


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
logProces()

# Funkcija brise tablice radi nove iteracije, ali prvo provjeri dali je tablica prazna!
def brisem(tablica):
    cursor = conn.cursor()
    sql = "SELECT count(*) as tot FROM %s;"%tablica
    cursor.execute(sql)
    data = cursor.fetchone()   
    for i in data:
        counts =  i
        
    if counts != 0:
        cursor_delete = conn.cursor()
        truncate = """truncate table """ + str(tablica) +str(' RESTART IDENTITY;') 
        cursor_delete.execute(truncate)
    conn.commit()  
  
# Ovdje brisem csv file iz kojeg kopiram u tablicu, pa ga ponovno kreiram za sljedecu iteraciju!
os.system("rm -rf /tmp/mycsvfile.csv")
os.system("touch /tmp/mycsvfile.csv")

# Ova funkcija gleda dali je korisnik upisao regex, pokupi i koristi taj regex u daljnjoj iteraciji!
def reSELECTOR():
    regexSELECTOR = conn.cursor()
    regexSELECTOR.execute("SELECT regex FROM application_regex WHERE status='not done';")
    conn.commit()
    for selector in regexSELECTOR:     
        if selector not in ('', None):
            return selector

# Ova Funkicja radi parsanje loga
def process_wrapper(chunkStart, chunkSize):
    reg = reSELECTOR()    
    if reg not in ('', None):
        for userRegex in reg:
            string = r'%s'%userRegex        
        pattern = re.compile(string)
    else:
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

# multitherading mode            
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
try:
    pool = mp.Pool(1)
    jobs = []


    for chunkStart, chunkSize in chunkify(danasnji_log):
        jobs.append(pool.apply_async(process_wrapper, (chunkStart, chunkSize)))
    for job in jobs:
        job.get()
    pool.close()
except:
    print 'problem multithreading'


#  Ovdje brisem glavnu tablicu i pozivam PL funkciju koja radi copy iz csv fajla u ovu rablicu, te postavljam korisnicki resetiram korisnicki regex
#  za sljdecu itraciju, naravno ako korisnik bude pisao vlastiti regex pri pokretanju parsera! 
brisem('application_nginxlog')
cur = conn.cursor()
print 'obriso sam, sada radim select procesing'
cur.execute("SELECT * FROM function_csv();")
regexHANDLER = conn.cursor()
regexHANDLER.execute("UPDATE application_regex SET status='done', regex='' WHERE id= 1;")
conn.commit()


def promet_vrijeme():
    print "F-ja: promet_vrijeme"
    try:
        brisem('application_vrijeme_promet')
        cursor2 = conn.cursor('cursor2')
        cursor2.itersize = 100000
        cursor2.execute("SELECT bandwidth, vrijeme FROM application_nginxlog")
        cptLigne = 0
        vrijeme_promet = {}
        dict_list = []
        cursor3 = conn.cursor()
        for rec in cursor2:
            cptLigne += 1
            time = rec[1].strftime('%Y-%b-%d %H:%M')
            promet = rec[0]
            dicts = {'vrijeme': time, 'promet': promet}
            dict_list.append(dicts)
            if cptLigne % 100000 == 0:
                #print '% 100000 == 0' + str(cptLigne)
                for item in dict_list:
                    vrijeme_promet[item['vrijeme']] = 0                    
                for item in dict_list:
                    vrijeme_promet[item['vrijeme']] += item['promet']            
                for key, values in sorted(vrijeme_promet.items()):
                    cptLigne += 1
                    vrijeme = key
                    promet = values           
                    query = "INSERT INTO application_vrijeme_promet(vrijeme, promet) VALUES (%s, %s);"
                    data = (vrijeme, promet)
                    cursor3.execute(query, data)                
                vrijeme_promet = None
                dict_list = None
                vrijeme_promet = {}
                dict_list = []    
        cursor2.close()
        cursor3.close()
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
        cursor4.close()
        conn.commit()
        for record in snipet_lista:
            snipet_promet[record['vrijeme']] = 0
        for record in snipet_lista:
            snipet_promet[record['vrijeme']] += record['promet']
        brisem('application_vrijeme_promet')
        cursor6 = conn.cursor()
        for key, values in sorted(snipet_promet.items()):            
            vrijeme = key
            promet_bayte = int(values)
            #our_value = Decimal(promet_bayte/1048576)
            #promet = Decimal(our_value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
            promet = promet_bayte/1048576
            #promet= ("%.3f" % our_value)            
            query = "INSERT INTO application_vrijeme_promet(vrijeme, promet) VALUES (%s, %s);"
            data = (vrijeme, promet)
            cursor6.execute(query, data)
        cursor6.close()
        conn.commit()
    except:
        print 'Error tijekom izvrsavanje funkcije jer je prazna tablica (promet_vrijeme)'       
promet_vrijeme()


# F-ja kolicina prometa u jedinici vremena, isto gore samo sto ovdje racuna sve upitom na bazu!
def promet_vrijemeSQL():
    print "F-ja: promet_vrijeme"
    brisem('application_vrijeme_promet')
    cursor2 = conn.cursor('cursor2')
    
    cursor2.execute("SELECT sum(bandwidth), to_char(vrijeme, 'YYYY-Mon-DD HH24:MI') from application_nginxlog  GROUP BY to_char DESC;")
    cursor6 = conn.cursor()

    for rec in cursor2:
        prom = rec[0]
        vrijeme = rec[1]
        promet = prom/1048576      
 
        query = "INSERT INTO application_vrijeme_promet(vrijeme, promet) VALUES (%s, %s);"
        data = (vrijeme, promet)
        cursor6.execute(query, data)
    cursor2.close()
    cursor6.close()
    conn.commit()
   
# F-ja broj requesta u jedinici vremena, racuna sve upitom na bazu
def request_vrijemeSQL():
    print "F-ja: request_vrijeme"
    brisem('application_requests_vrijeme')
    cursor7 = conn.cursor('cursor7')
    
    cursor7.execute("SELECT  count(*), to_char(vrijeme, 'YYYY-Mon-DD HH24:MI') from application_nginxlog  GROUP BY to_char DESC;")
   
    cursor8 = conn.cursor()
    for rec in cursor7:
        requests = rec[0]
        vrijeme = rec[1]     
                
        query = "INSERT INTO application_requests_vrijeme(vrijeme, requests) VALUES (%s, %s);"
        data = (vrijeme, requests)
        cursor8.execute(query, data)

    cursor7.close()
    cursor8.close()
    conn.commit()    


def request_vrijeme():
    print "F-ja: request_vrijeme"
    try:
        brisem('application_requests_vrijeme')
        cursor7 = conn.cursor('cursor7')
        cursor7.itersize = 100000
        cursor7.execute("SELECT vrijeme FROM application_nginxlog")
        cptLigne = 0
        lista_dictionaries = []
        request = {}
        cursor8 = conn.cursor()
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
                    query = "INSERT INTO application_requests_vrijeme(vrijeme, requests) VALUES (%s, %s);"
                    data = (vrijeme, requests)
                    cursor8.execute(query, data)
                request = None
                lista_dictionaries = None
                lista_dictionaries = []
                request = {}
        cursor7.close()
        cursor8.close()
        conn.commit()
        cursor9 = conn.cursor('cursor7')
        cursor9.execute("SELECT vrijeme, requests FROM application_requests_vrijeme")
        vrijeme_requestt = []
        vrijeme_req = {}
        cursor11 = conn.cursor()
        for items in cursor9:
            vrijeme = items[0]
            requesti = items[1]
            dicts = {'vrijeme': vrijeme, 'requests': requesti}
            vrijeme_requestt.append(dicts)
        for item in vrijeme_requestt:
            vrijeme_req[item['vrijeme']] = 0
        for item in vrijeme_requestt:
            vrijeme_req[item['vrijeme']] += item['requests']
        cursor9.close()
        conn.commit()
        brisem('application_requests_vrijeme')
        for vrijeme, requests in sorted(vrijeme_req.items()):            
            query = "INSERT INTO application_requests_vrijeme(vrijeme, requests) VALUES (%s, %s);"
            data = (vrijeme, requests)
            cursor11.execute(query, data)
        cursor11.close()
        conn.commit()
    except:
        print 'Error tijekom izvršavanja funkcije zato jer je tablica prazna! (request_vrijeme)'  
request_vrijeme()


# F-ja koliko koji IP generira requesta, prikazujem samo ako je broj requesta po IPu veci od 500
def najaktivniji_IP():
    print "F-ja: najaktivniji_IP"
    try:
        brisem('application_najaktivniji')
        cursor_ip = conn.cursor('cursor_ip')
        cursor_ip.execute("SELECT ip, count(*) FROM application_nginxlog GROUP BY ip")

        cursor_userInput = conn.cursor('cursor_userInput')
        cursor_userInput.execute("SELECT userdefineminimalrequest FROM application_overall")

        for x in cursor_userInput:
            for value in x:                          
                uservalue = value
        print uservalue
        if uservalue not in ('', None):
            print 'usao sam u user mod'+str(uservalue)
            cursor_stat1 = conn.cursor()
            for item in cursor_ip:
                ip = item[0]
                brojponavljanja = item[1]
                if brojponavljanja >= uservalue:                
                    query = "INSERT INTO application_najaktivniji(ip, brojponavljanja) VALUES (%s, %s);"
                    data = (ip, brojponavljanja)
                    cursor_stat1.execute(query, data)
        else:
            cursor_stat2 = conn.cursor()   
            for item in cursor_ip:
                ip = item[0]
                brojponavljanja = item[1]
                query = "INSERT INTO application_najaktivniji(ip, brojponavljanja) VALUES (%s, %s);"
                data = (ip, brojponavljanja)
                cursor_stat2.execute(query, data)
        conn.commit()
    except Exception as e:
        logging.error(traceback.format_exc())
najaktivniji_IP()


def get_content():
    try:
        print "F-ja: get_content"
        brisem('application_contents')
        cursor_ip = conn.cursor('statuss')
        cursor_ip.execute("SELECT request, count(*) FROM application_nginxlog GROUP BY request")

        cursor_userInput = conn.cursor('cursor_userInput')
        cursor_userInput.execute("SELECT userdefineminimalrequest FROM application_overall")
        for x in cursor_userInput:
            for value in x:                            
                uservalue = value                
        print uservalue
        if uservalue not in ('', None): 
            print 'usao sam u user mod'+str(uservalue)           
            cursor_stat1 = conn.cursor()
            for item in cursor_ip:
                content = item[0]
                brojponavljanja = item[1]
                if brojponavljanja >= uservalue:              
                    query = "INSERT INTO application_contents(content, brojponavljanja) VALUES (%s, %s);"
                    data = (content, brojponavljanja)
                    cursor_stat1.execute(query, data)
        else:
            cursor_stat = conn.cursor()
            for item in cursor_ip:
                content = item[0]
                brojponavljanja = item[1]                
                query = "INSERT INTO application_contents(content, brojponavljanja) VALUES (%s, %s);"
                data = (content, brojponavljanja)
                cursor_stat.execute(query, data)        

        conn.commit()
    except Exception as e:
        logging.error(traceback.format_exc())
get_content()


def ip_content():
    try:
        print "F-ja: ip_content"
        brisem('application_ipContent')
        cursor_ipContent = conn.cursor('ipContent')
        cursor_ipContent.execute("SELECT ip FROM application_najaktivniji;")
        args = []
        for ips in cursor_ipContent:
            ip = ips[0]
            args.append(ip)
        cursor_stat = conn.cursor()
       
        sql='SELECT request, count(*), ip FROM application_nginxlog WHERE ip IN (%s) GROUP BY request, ip;'
        in_p=', '.join(map(lambda x: '%s', args))
        sql = sql % in_p
        cursor_stat.execute(sql, args)
        cursor_insertt = conn.cursor()
        for items in cursor_stat:
            contents = items[0]
            counts = items[1]
            clients = items[2]
            #print clients, contents, counts    
            query = "INSERT INTO application_ipcontent(ip, content, counts) VALUES (%s, %s, %s);"
            data = (clients, contents, counts )
            cursor_insertt.execute(query, data)    
        cursor_insertt.close()
        conn.commit()
    except:
        print 'Error fun-ca ip_content'

ip_content()


# F-ja broj requsta po status kodovima
def access_by_Response_code():

    print "F-ja: access_by_Response_code"
    brisem('application_status')
    cursor_response = conn.cursor('cursor_response')
    cursor_response.execute("SELECT status, count(*) FROM application_nginxlog GROUP BY status")
    cursor_insert = conn.cursor()
    for statusi in cursor_response:
        status = statusi[0]
        brojponavljanja = statusi[1]   
        query = "INSERT INTO application_status(status, brojponavljanja) VALUES (%s, %s);"
        data = (status, brojponavljanja)
        cursor_insert.execute(query, data)  
    cursor_insert.close()
    conn.commit()

access_by_Response_code()


# F-ja koja racuna broj 200, 404, 206 requesta u jedinici vremena
def status_per_hour(code):
    try:
        print 'F-ja status_per_hour'
        tablica = "application_status_per_hour"+str(code)+str('(time, y) VALUES (%s, %s);')
        delete_table = "application_status_per_hour"+str(code)
        brisem(delete_table)
        statushour = conn.cursor('statushour')
        select = "SELECT status, count(*), to_char(vrijeme, 'YYYY-Mon-DD HH24') from application_nginxlog where status = '%s' GROUP BY to_char, status;"%str(code)
        statushour.execute(select) 
        ukupnaLista  = []
        onlydateList = []
        definedList  = []
        cursor_hour2 = conn.cursor()
        cursor_hour3 = conn.cursor()
        statushours = conn.cursor('statushours')
        for x in statushour:
            time = x[2] 
            ponavljanje = x[1]
            onlydate = x[2][:11]
            
            dodati = time, ponavljanje
            onlydateList.append(onlydate)
            ukupnaLista.append(dodati)
        if ukupnaLista:        
            #print("List is not empty")
            uniqueDate = list(set(onlydateList))
            for item in uniqueDate:        
                count = 0                
                while (count < 24):
                    counter = '%02d' % count
                    datum = item +" "+ str(counter)
                    definedList.append(datum)
                    count = count + 1

            for defined in definedList:
                if defined not in (item[0] for item in ukupnaLista):            
                    dodajem = defined, 0
                    ukupnaLista.append(dodajem)              
              
            ukupnaLista.sort()
            #(int(item[1]) for item in ukupnaLista)
            
            for items in ukupnaLista:
                time = items[0]+str(':00')
                y = int(items[1])                 
                insert = "INSERT INTO " +str(tablica)
                data = (time, y)
                cursor_hour2.execute(insert, data) 
        else:
            #print 'List is empty'
            #print tablica
            lista_fix = []
            
            select = "SELECT time, y from application_status_per_hour200;"
            statushours.execute(select)
            
            for x in statushours:
                time = x[0] 
                ponavljanje = 0
                za_dodati = time, ponavljanje
                lista_fix.append(za_dodati)
            for items in lista_fix:
                time = items[0]
                y = int(items[1])                       
                insert = "INSERT INTO " +str(tablica)
                data = (time, y)
                cursor_hour3.execute(insert, data)
                  
        conn.commit()
    except:
        print 'Prethodne Funkcije su bile prazne pa je ovaj select prazan! (status_per_hour)'

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

try:
    brisem('application_document')
except:
    print 'Pokusavam obrisati application_document'


def fixTable():
    try:
        print 'F-ja fixTable'
        statushours200 = conn.cursor('statushours200')           
        select = "SELECT time, y from application_status_per_hour200;"
        statushours200.execute(select)

        ukupno200 = []
        for f in statushours200:
            vrijeme = f[0]
            ponavljanje = f[1]
            
            ukupno200.append(vrijeme)
            
        
        statushours200.close()
        conn.commit()
        ######################################################
        statushours206 = conn.cursor('statushours206')      
        select206 = "SELECT time, y from application_status_per_hour206;"
        statushours206.execute(select206)
        ukupno206 = []
        ukupnopomocni = []
        for f in statushours206:
            vrijeme = f[0]             
            ponavljanje = f[1]
            ukupno2 = vrijeme, ponavljanje
            ukupnopomocni.append(vrijeme)      
            ukupno206.append(ukupno2)

        for var200 in ukupno200:
            if var200 not in ukupnopomocni:
                y = 0
                suma1 = var200, y                    
                ukupno206.append(suma1)
       
        statushours206.close()
        conn.commit()
        brisem('application_status_per_hour206')
        ukupno206.sort()
        for j in ukupno206:
            time = j[0]
            y = j[1]
            cursor_insertt = conn.cursor()
            query = "INSERT INTO application_status_per_hour206(time, y) VALUES ( %s, %s);"
            data = (time, y)
            cursor_insertt.execute(query, data)     
        cursor_insertt.close()
        conn.commit()
        #####################################################
        statushours404 = conn.cursor('statushours404')      
        select404 = "SELECT time, y from application_status_per_hour404;"
        statushours404.execute(select404)
        ukupno404 = []
        ukupnopomocni = []
        for f in statushours404:
            vrijeme = f[0]             
            ponavljanje = f[1]
            ukupno2 = vrijeme, ponavljanje
            ukupnopomocni.append(vrijeme)      
            ukupno404.append(ukupno2)
        for var200 in ukupno200:
            if var200 not in ukupnopomocni:
                y = 0
                suma1 = var200, y                    
                ukupno404.append(suma1)        
        statushours404.close()
        conn.commit()
        brisem('application_status_per_hour404')
        ukupno404.sort()
        cursor_insertt = conn.cursor()
        for j in ukupno404:
            time = j[0]
            y = j[1]
            
            query = "INSERT INTO application_status_per_hour404(time, y) VALUES ( %s, %s);"
            data = (time, y)
            cursor_insertt.execute(query, data)     
        cursor_insertt.close()
        conn.commit()
    except:
        print 'Prethodne funkcije su bile prazne! (fixTable)'

fixTable()


def nginx_graphOne():
    try:
        queryset = []
        brisem('application_overall')
        queryset1 = conn.cursor('queryset1')      
        queryset1.execute ("SELECT count(status) from application_nginxlog where status = 400;")
       

        queryset2 = conn.cursor('queryset2')      
        select2  = "SELECT count(status) from application_nginxlog where status = 404;"
        queryset2.execute(select2)

        queryset3 = conn.cursor('queryset3')      
        select3  = "SELECT count(status) from application_nginxlog where status = 200;"
        queryset3.execute(select3)


        queryset4 = conn.cursor('queryset4')      
        select4  = 'SELECT count(status) from application_nginxlog;'
        queryset4.execute(select4)

        queryset5 = conn.cursor('queryset5')      
        select5  = 'SELECT count(distinct ip) from application_najaktivniji;'
        queryset5.execute(select5)

        queryset6 = conn.cursor('queryset6')      
        select6  = 'SELECT  count(distinct content) from application_contents;'
        queryset6.execute(select6)

        queryset7 = conn.cursor('queryset7')      
        select7 = "SELECT count(status) from application_nginxlog where status = 405;"
        queryset7.execute(select7)

        queryset8 = conn.cursor('queryset8')      
        select8 = 'SELECT sum(promet) from application_vrijeme_promet;'
        queryset8.execute(select8)

        queryset9 = conn.cursor('queryset9')      
        select9 = 'SELECT status from application_status;'
        queryset9.execute(select9)
          
        queryset10 = os.path.getsize('/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/access.log') 

        queryset11 = conn.cursor('queryset11')      
        select11 = "SELECT count(status) from application_nginxlog where status = 403;"
        queryset11.execute(select11)
       
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


        def humansize(nbytes):
            
            if nbytes == 0: return '0 B'
            i = 0
            while nbytes >= 1024 and i < len(suffixes)-1:
                nbytes /= 1024.
                i += 1
            f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
            size = str('%s %s' % (f, suffixes[i]))

            fileSize = {'fajl': size}
            queryset.append(fileSize)

        humansize(queryset10)
        for v in queryset8:
            value = int(v[0])
            
            if value < 1024:       
                
                prometMege= value+str(' MB')                
                prometM = {'promet':prometMege}
                queryset.append(prometM)
            else:
                our_valueGige = value/1024
                
                prometGige = ("%.3f" % our_valueGige)+str(' GB')
           
                prometG = {'promet':prometGige}

                queryset.append(prometG)        

        for p in queryset3:
            val = int(p[0])
            code200 = {'code200': val}
            queryset.append(code200)

        
        for l in queryset2:
            val1 = int(l[0])
            code404 = {'code404': val1}
            queryset.append(code404)

        
        for n in queryset5:
            val2 = int(n[0])

            ip = {'ip': val2}
            queryset.append(ip)


        for j in queryset6:
            val3 = int(j[0])
            content = {'content': val3}
            queryset.append(content)
            humansize(queryset10)
        
        for i in queryset9:
            statusi = int(i[0])
            dodati = {'code': statusi}
            queryset.append(dodati)

        for k in queryset4:
            val4 = int(k[0])
            total = {'total': val4}
            queryset.append(total)

        for z in queryset7:
            val5 = int(z[0])
            static = {'metod': val5}
            queryset.append(static)


        for w in queryset1:
            val6 = int(w[0])
            status400 = {'status400': val6}
            queryset.append(status400)

        for h in queryset11:
            val7 = int(h[0]) 
            status403 = {'status403': val7}
            queryset.append(status403)
        conn.commit()   
        
        cur = conn.cursor()
        insert_statement = 'insert into application_overall (%s) values %s;'
        #print queryset
        for mydict in queryset:
            columns = mydict.keys()
            values = [mydict[column] for column in columns]
            
            cur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            #print cur.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
        conn.commit()
    except:
        print 'Error overall (nginx_graphOne)'  

nginx_graphOne()


# Ova funkcija brise stari log, tj cisti za sljedecu uporabu.
def brisemStariLog():
    try:          
        name ='/home/Nginx_Log_Analyzer/nginx_log_analyzer_env/project/access.log'
        if os.path.isfile(name):                    
            y = name[56:]           
            files = open(y, "w")
            files.close()                        
            os.remove(name)
    except:
        print "Brisanje log file-a! (brisemStariLog)"

#brisemStariLog()

# Ovdje na kraju racunam i zapisujem vrijeme rada skripte

try:
    #print((time.time() - start_time))
    executionTime = (time.time() - start_time)   
    if executionTime > 60:
        timeinteger = executionTime / 60
        scripttime =  str(timeinteger) +' min'
        cursor_duration = conn.cursor()
        cursor_duration.execute("INSERT INTO application_overall(scriptTime) VALUES(%s)",(scripttime,)) 
       
    else:
        data = str(executionTime)+' s'
        cursor_duration2 = conn.cursor()
        cursor_duration2.execute("INSERT INTO application_overall(scriptTime) VALUES(%s)",(data,)) 
    conn.commit()
     
except Exception as e:
    logging.error(traceback.format_exc())


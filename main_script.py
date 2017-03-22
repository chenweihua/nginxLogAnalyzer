#!/usr/bin/nginx_log_analyzer_env python
# -*- coding: utf-8 -*-

'''
Author: Ivan Zilic

description:
-   This script performs parsing user log files and write results into the database!
-   Script use python multiprocessing, because we want faster  parse large log file (this is useful when we have a large file)!
-   Script call postgres PL function, (I wrote PL/SQL Function,  which use COPY method on postgres database) 
    for copy parsed data from CSV to database, because this is faster than insert one by one row in database (this is useful when we have a large file).
'''


from __future__ import division
import os
import re
import psycopg2
import multiprocessing as mp
import subprocess
import glob
import os.path
import sys
import csv
from psycopg2.extensions import AsIs
import time
import traceback
import logging
import urllib, json

start_time = time.time()

BASE_DIR = os.getcwd()


try:
    conn = psycopg2.connect("dbname='nginxbase' user='nginx' host='localhost' password='789ivanino'")
except:
    print "I am unable to connect to the database"


''' 
    log Process function checks number of uploaded log files, check file compression type, 
    and unpack files depending on compression type!
'''
def logProces(logfile, base_dir):
    print 'Function: logProces'
    try:
        fileexts = ['.tar.gz', '.gz', '.zip']
        upload_dir = base_dir+str('/upload/')
        character_count = len(upload_dir)
        path, dirs, files = os.walk(upload_dir).next()
        file_count = len(files)

        # Check if user upload more than one log!

        if file_count > 1:            
            upload_logs = glob.glob(upload_dir+str('*'))            
            for name in upload_logs:
                try:
                    # Check log file compres type (zip, tar.gz, gz, gunzip)!

                    for ext in fileexts:
                        if name.endswith(ext):                           
                            if ext == '.zip':
                                y = name[character_count:]                                             
                                filename = upload_dir+str(y)
                                subprocess.call(['unzip', '-j', '-o', filename, '-d', upload_dir])
                                os.remove(filename)
                            elif ext == '.tar.gz':
                                z = name[character_count:]               
                                filenamez = upload_dir+str(z)
                                subprocess.call(['tar', '-zxvf', filenamez, '-C', upload_dir])
                                os.remove(filenamez)
                            elif ext == '.gz':
                                c = name[character_count:]               
                                filenamez = upload_dir+str(c)
                                subprocess.call(['gunzip', filenamez])                                
                            else:
                                print "Uploaded file extension are not supported!"
                                sys.exit()                
                except:
                    print 'unzip error'
            #  Remove spaces and underscore from name of unzip files!

            upload_logs2 = glob.glob(upload_dir+str('*'))
            for unzipfile in upload_logs2:
                x = upload_logs2[character_count:]            
                filepath = upload_dir+str(x)
                os.rename(filepath, filepath.replace(" ", "_"))
            final_list = []

            upload_logs3 = glob.glob(upload_dir+str('*'))
            for files in upload_logs3:
                final_list.append(files)                 
            # write all log files in one access.log file!

            with open(logfile, "wb") as outfile:
                for f in final_list:
                    with open(f, "rb") as infile:
                        outfile.write("\n"+ infile.read())
            # When we done, remove unzip files from upload dir!

            upload_logs4 = glob.glob(upload_dir+str('*'))
            for files4 in upload_logs4:
                os.remove(files4)

        # User has uploaded 0 or one log file!
        else:
            try:                
                filelog = glob.glob(upload_dir+str('*'))
                for logs in filelog:
                    # Check log file compres type (zip, tar.gz, gz, gunzip)
                    for exty in fileexts:
                        if logs.endswith(exty):                           
                            if exty == '.zip':
                                subprocess.call(['unzip', '-j', '-o', logs, '-d', upload_dir])
                                os.remove(logs)
                                
                            elif exty == '.tar.gz':                
                     
                                subprocess.call(['tar', '-zxvf', logs, '-C', upload_dir])                       
                                os.remove(logs)
                            elif exty == '.gz':                
                     
                                subprocess.call(['gunzip', logs])                        
                                                                                 
                            else:
                                print "Uploaded file extension are not supported!"
                                sys.exit()
                filelogTar1 = glob.glob(upload_dir+str('*'))
                for itemOne in filelogTar1:
                    p = itemOne[character_count:]                    
                    old_f = upload_dir+str(p)
                    new_f = base_dir+str('/access.log')           
                    os.rename(old_f,new_f)
            except Exception as e:
                logging.error(traceback.format_exc())
    except Exception as e:
        logging.error(traceback.format_exc())
logProces('access.log', BASE_DIR)

'''
   This function check if specific table is empty if not then deletes this 
   table, because for each new analysis we need to have a blank table!
'''

def delete_table(table):
    cursor = conn.cursor()
    sql = "SELECT count(*) as tot FROM %s;"%table
    cursor.execute(sql)
    data = cursor.fetchone()   
    for i in data:
        counts =  i
        
    if counts != 0:
        cursor_delete = conn.cursor()
        truncate = """truncate table """ + str(table) +str(' RESTART IDENTITY;') 
        cursor_delete.execute(truncate)
    conn.commit()  
def check_empty_table(table):
    cursor = conn.cursor()
    sql = "SELECT count(*) as tot FROM %s;"%table
    cursor.execute(sql)
    data = cursor.fetchone()   
    for i in data:
        counts =  i
        
    if counts != 0:
        return False
    else:
        return True

    conn.commit()  
access_log = "access.log"  

''' 
    Parsed results are written in CSV, so for each new iteration we need a new file!
    Because we use SQL / PL function (that I written on Postgres database,which use 
    COPY method to make copy from csv file to database, because it is faster than 
    conventional insert line by line)!
'''

os.system("rm -rf /tmp/mycsvfile.csv")
os.system("touch /tmp/mycsvfile.csv")

''' 
    This function check if user write his own regex, for parsing log file!
    Because we allow user to write his own regex that will be used during 
    parse log file, but that regex will be use only once for that current 
    iteration because we must allow new regex for new users and new iteration. 
'''
print 'Parse log file'
def reSELECTOR():
    regexSELECTOR = conn.cursor()
    regexSELECTOR.execute("SELECT regex FROM application_regex WHERE status='not done';")
    conn.commit()
    for selector in regexSELECTOR:     
        if selector not in ('', None):
            return selector

'''
    This function parses a log file, but before that, function checks if user 
    has wrote his own regex, if user wrote his own regex function  will use it, 
    if not function has its own regex that will use!
'''
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
        with open(access_log) as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).splitlines()
            for line in lines:
                for m in re.finditer(pattern, line):                   
                    ip        =   m.group(1)
                    time      =   m.group(2)                               
                    request   =   m.group(4)
                    status    =   m.group(5)
                    bandwidth =   m.group(6)                    
                    referrer  =   m.group(7)
                    user_agent=   m.group(8)                 
                    writer.writerow( (ip, time, request, status, bandwidth, user_agent, referrer) )     
    finally:
        f.close()

''' This is multiprocessing mode, we use python multiprocessing because we want faster parse large log file.'''

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

    for chunkStart, chunkSize in chunkify(access_log):
        jobs.append(pool.apply_async(process_wrapper, (chunkStart, chunkSize)))
    for job in jobs:
        job.get()
    pool.close()
except Exception as e:
    logging.error(traceback.format_exc())


'''
    Now we call postgres PL/SQ function, (function use COPY method on postgres database, 
    for  copy parsed data from CSV file to database), because this is faster than insert one by one row 
    (this is useful when we have a large file). If user has writen his own regex, and we used it, but in this part we 
    must update this field from 'not done' to 'done', because we must know in next iteration a regex was used once, and 
    no more, this option allow user for new iteration to write new regex that will be used instead this old regex.
'''
delete_table('application_nginxlog')
cur = conn.cursor()
cur.execute("SELECT * FROM function_csv();")
regexHANDLER = conn.cursor()
regexHANDLER.execute("UPDATE application_regex SET status='done', regex='' WHERE id= 1;")
conn.commit()

'''
    This function calculate traffic per minute (MB/min), function count all client request per minutes 
    and count the traffic that the server generates per minute.If we have large file, we don't want use
    whole RAM memory of our server, during load data into memory, so we process <= 100000 rows in the one part!
'''
def traffic_per_minute():
    print 'Function: traffic_per_minute'    
    try:
        delete_table('application_vrijeme_promet')
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
            if cptLigne <= 100000:               
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
        # We must check if we have duplicated minute in same hour!

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
        delete_table('application_vrijeme_promet')
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
    except Exception as e:
        logging.error(traceback.format_exc())     
traffic_per_minute()

'''
    This function calculate clients request per minute, if we have large file, we don't 
    want use whole RAM memory of our server, during load data into memory, so we process 
    <= 100000 rows in the one part!    
'''

def request_per_minute():
    print 'Function: request_per_minute'    
    try:
        delete_table('application_requests_vrijeme')
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
            if cptLigne <= 100000:            
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
        delete_table('application_requests_vrijeme')
        for vrijeme, requests in sorted(vrijeme_req.items()):            
            query = "INSERT INTO application_requests_vrijeme(vrijeme, requests) VALUES (%s, %s);"
            data = (vrijeme, requests)
            cursor11.execute(query, data)
        cursor11.close()
        conn.commit()
    except Exception as e:
        logging.error(traceback.format_exc())   
request_per_minute()

'''
    This function calculate number of request per specific client, in this function there is option which check if user
    are defined number of request per specific client, if not, function calculate number of request for all clients (this is not
    good option if we have large access.log file 1GB, because performing duration may take longer)! 
'''
def most_active_IP():
    print 'Function: most_active_IP'    
    try:
        delete_table('application_najaktivniji')
        cursor_ip = conn.cursor('cursor_ip')
        cursor_ip.execute("SELECT ip, count(*) FROM application_nginxlog GROUP BY ip")
        cursor_userInput = conn.cursor('cursor_userInput')
        cursor_userInput.execute("SELECT userdefineminimalrequest FROM application_overall")

        uservalue = check_empty_table('application_overall')
        if uservalue not in ('', None, False):
            cursor_stat1 = conn.cursor()
            for item in cursor_ip:
                ip = item[0]
                brojponavljanja = item[1]
                if brojponavljanja >= cursor_userInput:                
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
most_active_IP()

''' This function calculate content frequency request (number of request per specific content)! '''
def get_content():
    print 'Function: get_content'
    try:
        delete_table('application_contents')
        cursor_ip = conn.cursor('statuss')
        cursor_ip.execute("SELECT request, count(*) FROM application_nginxlog GROUP BY request")
        cursor_userInput = conn.cursor('cursor_userInput')
        cursor_userInput.execute("SELECT userdefineminimalrequest FROM application_overall")

        uservalue = check_empty_table('application_overall')
        if uservalue not in ('', None, False):
            cursor_stat1 = conn.cursor()
            for item in cursor_ip:
                content = item[0]
                brojponavljanja = item[1]
                if brojponavljanja >= cursor_userInput:              
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

''' This function calculate content frequency request per specific client (number of content request per specific client)! '''
def ip_content():
    print 'Function: ip_content'

    try:
        delete_table('application_ipContent')
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
            query = "INSERT INTO application_ipcontent(ip, content, counts) VALUES (%s, %s, %s);"
            data = (clients, contents, counts )
            cursor_insertt.execute(query, data)    
        cursor_insertt.close()
        conn.commit()
    except Exception as e:
        logging.error(traceback.format_exc())

ip_content()

''' This function shows number of specific status code (status code: 200, 404, 500, 206...etc) ''' 
def access_by_Response_code():
    print 'Function: access_by_Response_code'

    delete_table('application_status')
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

''' This function calculate specific status code per hour! '''
def status_per_hour(code):
    print 'Function: status_per_hour'

    try:
        tablica = "application_status_per_hour"+str(code)+str('(time, y) VALUES (%s, %s);')
        delete_tabs = "application_status_per_hour"+str(code)
        delete_table(delete_tabs)
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
            for items in ukupnaLista:
                time = items[0]+str(':00')
                y = int(items[1])                 
                insert = "INSERT INTO " +str(tablica)
                data = (time, y)
                cursor_hour2.execute(insert, data) 
        else:
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
    except Exception as e:
        logging.error(traceback.format_exc())

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
    delete_table('application_document')
except Exception as e:
    logging.error(traceback.format_exc())


def fixTable():
    print 'Function: fixTable'
    try:
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
        delete_table('application_status_per_hour206')
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
        delete_table('application_status_per_hour404')
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
    except Exception as e:
        logging.error(traceback.format_exc())

fixTable()

''' This function calculate overal informations of analyzing log file:
    Total request, valid request, Not found request, unique visitors, unique files, 
    Forbidden request, bad request, log Size, bandwidth, mwthod not allowed, status code and proc. time    
'''
def nginx_graphOne():
    print 'Function: nginx_graphOne'
    try:
        queryset = []
        delete_table('application_overall')
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
        logfile = BASE_DIR+str('/access.log')  
        queryset10 = os.path.getsize(logfile) 

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
        conn.commit()
    except Exception as e:
        logging.error(traceback.format_exc())

nginx_graphOne()

''' This function delete access log, because for new iteration we use new log file that users upload!'''
def delete_access_log(file):
    try:          
        name =file+str('access.log')
        if os.path.isfile(name):                    
            y = name[56:]           
            files = open(y, "w")
            files.close()                        
            os.remove(name)
    except Exception as e:
        logging.error(traceback.format_exc())

delete_access_log(BASE_DIR)

''' We also provide an option with geolocation of specifc IP address
    (if IP is public), but first we must catch IP adress from user log file
    and write this IP address into file, so this function make file with range of 
    IP for geoblocing, and after that function call another script which made geolocation
    on the world map, and this function generate two png images,  one for 'valid' user request,
    and one for 'not valid' user request.
'''

def range_ip_for_geolocation(files):
    ip_api_url = 'http://applicationfree.net:8080/najaktivniji/?format=json'
    response = urllib.urlopen(ip_api_url)
    data = json.loads(response.read())
    filename = str('/')+str(files)

    file_path = BASE_DIR+str(filename)
    my_file = os.path.exists(file_path)
    print my_file
    if my_file != 'False':
        try:
            os.remove(files)
        except:
            print 'ip file '+str(files)

    outfile = open(files, "w+")
    for ip_dictionary in data:
        ip_range = dict((key,value) for key, value in ip_dictionary.iteritems() if key == 'ip')
        for key, value in ip_range.iteritems():
            print >> outfile, value
    outfile.close()
    os.system("python geoip.py -i ip.txt --service m --db GeoLiteCity.dat --output='application/static/img/valid.png'")
    os.system("python geoip.py -i ip.txt --service m --db GeoLiteCity.dat --output='application/static/img/notvalid.png'")
range_ip_for_geolocation('ip.txt')


# Calculate script running time!
try:
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


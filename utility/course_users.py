#!/home/tahoe/.virtualenvs/edx-platform/bin/python
# -*-coding:utf-8-*-

import os,sys,getopt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms.envs.cms.staging")
os.environ.setdefault("SERVICE_VARIANT", 'lms')

home=os.path.expanduser("~/") 
sys.path.append(home+"edx_all/edx-platform/")
sys.path.append(home+"edx_all/")

import lms.envs.cms.staging, django
django.conf.settings=lms.envs.cms.staging

django.conf.settings.DATABASE_ROUTERS =        []                                                         
django.conf.settings.URL_VALIDATOR_USER_AGENT= "Django/1.4.5 (https://www.djangoproject.com)"               
django.conf.settings.DEFAULT_INDEX_TABLESPACE= ""                                                          
django.conf.settings.DEFAULT_TABLESPACE=       ""                                                         
django.conf.settings.DATETIME_FORMAT=          "N j, Y, P"                                                  
django.conf.settings.DATE_FORMAT=              "N j, Y"                                                     
django.conf.settings.TIME_FORMAT=              "P"                                                          
django.conf.settings.YEAR_MONTH_FORMAT=        "F Y"                                                        
django.conf.settings.MONTH_DAY_FORMAT=         "F j"                                                        
django.conf.settings.TRANSACTIONS_MANAGED=     False                                                      
django.conf.settings.FORCE_SCRIPT_NAME=        None                                                       
django.conf.settings.ALLOWED_HOSTS =           ['*']

from path import path
import lms.startup as startup
from django.contrib.auth.models import User
from django.conf import settings
from courseware.courses import get_course_with_access, get_course_by_id
from courseware.model_data import FieldDataCache
from courseware import grades

from StringIO import StringIO
from django.core.handlers.wsgi import WSGIRequest

# =======================================================

from datetime import datetime
from elasticsearch import Elasticsearch
import MySQLdb
from pymongo import Connection

# =======================================================

django.conf.settings.MITX_FEATURES['ENABLE_SQL_TRACKING_LOGS'] = False
import logging
logging.disable(logging.ERROR)
#logging.disable(logging.INFO) logging.CRITICAL
#logging.disable(logging.WARNING)

import warnings
warnings.simplefilter("ignore")

# =======================================================

def fake_get(path='/', user=None):
    req = WSGIRequest({'REQUEST_METHOD': 'GET', 'PATH_INFO': path, 'wsgi.input': StringIO()})
    from django.contrib.auth.models import AnonymousUser
    req.user = AnonymousUser() if user is None else user
    req.session={}
    req.META={'SERVER_NAME':'staging.pepperpd.com','SERVER_PORT':'80',}
    return req

def mongo_conn(host='localhost', db='xmodule', port=27017, user=None, password=None, **kwargs):
    db = Connection(host=host, port=port, **kwargs)[db]
    if user is not None and password is not None:
        db.authenticate(user, password)
    return db

def mysql_conn():
    db = MySQLdb.connect(host="localhost", user="pepper", passwd="lebbeb", db="pepper")
    return db

def mysql_exesql(sql,param):
    db=mysql_conn()
    db.cursor().execute(sql,param)
    db.commit()
    db.close()

def mysql_fetch_all(sql):
    db=mysql_conn()
    cursor=db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result

def mysql_fetch_one(sql):
    db=mysql_conn()
    cursor=db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    return result

def cohort_district(id):
    result=mysql_fetch_one("SELECT a.name from district a inner join cohort b on a.id=b.district_id where b.id=%s;" % id)
    if result:
        return result[0]

def school_name(id):
    result=mysql_fetch_one("SELECT name from school where id=%s;" % id)
    if result:
        return result[0]

def cohort_code(id):
    result=mysql_fetch_one("SELECT code from cohort where id=%s;" % id)
    if result:
        return result[0]    

from xmodule.course_module import CourseDescriptor
from xmodule.modulestore.django import modulestore
from courseware.grades import grade
from django.contrib.auth.models import User

def course_from_id(course_id):
    """Return the CourseDescriptor corresponding to this course_id"""
    course_loc = CourseDescriptor.id_to_location(course_id)
    return modulestore().get_instance(course_id, course_loc)    

def score(course_id,user_id):
    request=fake_get()
    
    student=User.objects.get(id=user_id)
    # course=get_course_by_id(course_id)
    course=course_from_id(course_id)

    # field_data_cache = FieldDataCache.cache_for_descriptor_descendents(course_id, student, course, depth=None)
    # grade_summary = grades.grade(student,request , course, field_data_cache)
    # progress="{totalscore:.0%}".format(totalscore=grade_summary['percent'])

    progress=grade(student,request,course)['percent']

    return '1' if grade_summary['percent']>=0.85 else '0' 

def get_course_ids(want=None):
    if want:
        return want.replace(' ','').split(',')
    
    db=mongo_conn()
    courses=[]
    
    for c in db.modulestore.find({"_id.category" : "course"}): #
        _id=c.get("_id")
        course_id="%s/%s/%s" % (_id.get('org'), _id.get('course'), _id.get('name'))
        courses.append(course_id)
    return courses

SQL_COUNT_USER="SELECT count(*) from auth_user a inner join auth_userprofile b on a.id=b.user_id where a.is_active %s";
SQL_USER="SELECT a.id,a.username,b.cohort_id,a.first_name,a.last_name,a.email,b.school_id from auth_user a inner join auth_userprofile b on a.id=b.user_id where a.is_active %s limit %s,%s;"
SQL_USER_COURSE="SELECT a.course_id from student_courseenrollment a where a.is_active and a.user_id=%s;"

def status(start,end,district_id=None,courses=None):
    courses=get_course_ids(courses)


    for c in courses:
        sys.stdout.write("registered|progress|pass|")

    sys.stdout.write("district|school|user id|first name|last name|user name|email|cohort\n")
    
    def user(user_id,username,cohort_id,first_name,last_name,email,school_id):
        user_courses={}
        result=mysql_fetch_all(SQL_USER_COURSE % (user_id))
        for record in result:
            course_id=record[0]
            if course_id in courses:
                user_courses[course_id]=1

        for cid in courses:
            p='Y' if user_courses.get(cid) else 'N'
            scr=http_get_score(cid,username)
            if scr!='E':
                pas='Y' if int(scr)>=85 else 'N'
            else:
                pas='E'
            sys.stdout.write("%s|%s%%|%s|" % (p,scr,pas))
            
        sys.stdout.write ("%s|%s|%s|%s|%s|%s|%s|%s\n" % (cohort_district(cohort_id)
                                                          ,school_name(school_id)
                                                          ,user_id
                                                          ,first_name
                                                          ,last_name
                                                          ,username
                                                          ,email
                                                          ,cohort_code(cohort_id)
                                                          ))
        sys.stdout.flush()

    cond=''
    if district_id:
        cond='and b.cohort_id in (select id from cohort where district_id=%s)' % district_id

    result=mysql_fetch_all(SQL_USER % (cond,start-1,end-start+1))

    for u in result:
        user(u[0],u[1],u[2],u[3],u[4],u[5],u[6]);

def user_count(district_id=None):
    cond=''
    if district_id:
        cond='and b.cohort_id in (select id from cohort where district_id=%s)' % district_id
    result=mysql_fetch_one(SQL_COUNT_USER % cond)
    print "user count:",result[0]

def course(courses=None):
    courses=get_course_ids(courses)
    for c in courses:
        print c

def http_get_score(course_id,username):
    score=''
    import httplib
    import re
    httpClient = None
    try:
        httpClient = httplib.HTTPConnection('localhost', 8000, timeout=30)
        httpClient.request('GET', '/instructor/dashboard/progress/%s/%s' % (course_id,username))
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        # print response.status
        # print response.reason
        content = response.read()
        m=re.search("progress:(\d+)",content)
        score='E' if not m else m.group(1) 
    except Exception, e:
        score="E"
    finally:
        if httpClient:
            httpClient.close()
    return score
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:d:s:e:c:l:",["cmd=","district=","start=","end=","lessions="])
    except getopt.GetoptError:
        print "invalid args."
        sys.exit(2)

    cmd=''
    district_id=''
    s,e='',''
    courses=''
    
    for opt, arg in opts:
      if opt in ("-c","--cmd"):
          cmd=arg
      elif opt in ("-d", "--district"):
          district_id=arg
      elif opt in ("-s", "--start"):
          s = arg
      elif opt in ("-e", "--end"):
          e = arg
      elif opt in ("-l", "--lessions"):
          courses = arg          

    # print cmd,district_id,s,e

    if cmd=='count':
        user_count(district_id)
    elif cmd=='courses':
        course(courses)
    elif cmd=='status':
        status(int(s),int(e),district_id,courses)
    else:
        print "invalid command"

if __name__ == '__main__':
    if sys.argv[1]=='-h' or sys.argv[1]=='--help':
        print """
# at first:
# workon edx-platform
# cd ~/edx_all/scripts/utility

# course_users.py args:
# -c|--cmd=       command      (count/courses/status)
# -d|--district=  district id  (optional, arg for count/status command)
# -s|--start=     paging start (arg for status command)
# -e|--end=       paging stop  (arg for status command)
# -l|--lessions=  course id    (optional, arg for courses/status command, quoted by "", splited by ,)

# example: count of student
# ./course_users.py -c count
# ./course_users.py -c count -d 10

# example: list of course
# ./course_users.py -c courses
# ./course_users.py -c courses -l \"WestEd/ELA101x/2014_Spring, WestEd/MA101x/2014_Spring\"

# example: get study status
# ./course_users.py -c status -d 10 -s 1 -e 2
# ./course_users.py -c status -d 10 -s 1 -e 2 -l \"WestEd/ELA101x/2014_Spring\"
        """
        exit(0)
    main(sys.argv[1:])

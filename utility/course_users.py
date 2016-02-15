#!/home/tahoe/.virtualenvs/edx-platform/bin/python
# -*-coding:utf-8-*-

import os,sys,getopt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms.envs.cms.staging")
os.environ.setdefault("SERVICE_VARIANT", 'lms')

home=os.path.expanduser("~/") 
sys.path.append(home+"edx_all/edx-platform/")
sys.path.append(home+"edx_all/edx-platform/lms/djangoapps")
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

from xmodule.course_module import CourseDescriptor
from xmodule.modulestore.django import modulestore
from courseware.grades import grade
from django.contrib.auth.models import User

# =======================================================

# def fake_get(path='/', user=None):
#     req = WSGIRequest({'REQUEST_METHOD': 'GET', 'PATH_INFO': path, 'wsgi.input': StringIO()})
#     from django.contrib.auth.models import AnonymousUser
#     req.user = AnonymousUser() if user is None else user
#     req.session={}
#     req.META={'SERVER_NAME':'staging.pepperpd.com','SERVER_PORT':'80',}
#     return req


def mongo_conn(host='localhost', db='xmodule', port=27017, user=None, password=None, **kwargs):
    db = Connection(host=host, port=port, **kwargs)[db]
    if user is not None and password is not None:
        db.authenticate(user, password)
    return db


def mysql_conn():
    db = MySQLdb.connect(host="localhost", user="pepper", passwd="lebbeb", db="pepper")
    return db


def mysql_exesql(sql, param):
    db = mysql_conn()
    db.cursor().execute(sql, param)
    db.commit()
    db.close()


def mysql_fetch_all(sql):
    db = mysql_conn()
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result


def mysql_fetch_one(sql):
    db = mysql_conn()
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    return result

# def cohort_district(id):
#     result=mysql_fetch_one("SELECT a.name from district a inner join cohort b on a.id=b.district_id where b.id=%s;" % id)
#     if result:
#         return result[0]


def school_name(id):
    result = mysql_fetch_one("SELECT name from school where id='%s';" % id)
    if result:
        return result[0]


def district_name(id):
    result = mysql_fetch_one("SELECT name from district where id='%s';" % id)
    if result:
        return result[0]

def cohort_code(id):
    result = mysql_fetch_one("SELECT code from cohort where id='%s';" % id)
    if result:
        return result[0]


# def course_from_id(course_id):
#     """Return the CourseDescriptor corresponding to this course_id"""
#     course_loc = CourseDescriptor.id_to_location(course_id)
#     return modulestore().get_instance(course_id, course_loc)


# def score(course_id, user_id):
#     request = fake_get()

#     student = User.objects.get(id=user_id)
#     # course=get_course_by_id(course_id)
#     course = course_from_id(course_id)

#     # field_data_cache = FieldDataCache.cache_for_descriptor_descendents(course_id, student, course, depth=None)
#     # grade_summary = grades.grade(student,request , course, field_data_cache)
#     # progress="{totalscore:.0%}".format(totalscore=grade_summary['percent'])

#     progress = grade(student, request, course)['percent']
#     return '1' if grade_summary['percent'] >= 0.85 else '0'


def get_course_ids(want=None):
    if want:
        return want.replace(' ', '').split(',')

    db = mongo_conn()
    courses = []

    for c in db.modulestore.find({"_id.category": "course"}):
        _id = c.get("_id")
        course_id = "%s/%s/%s" % (_id.get('org'), _id.get('course'), _id.get('name'))
        courses.append(course_id)
    return courses


SQL_COUNT_USER = "SELECT count(*) from auth_user a inner join auth_userprofile b on a.id=b.user_id where a.is_active %s;"

SQL_USER = "SELECT a.id,a.username,b.district_id,b.cohort_id,a.first_name,a.last_name,a.email,b.school_id,activate_date from auth_user a inner \
   join auth_userprofile b on a.id=b.user_id where a.is_active %s limit %s,%s;"

SQL_USER_COURSE = "SELECT a.course_id,a.created from student_courseenrollment a where a.is_active and a.user_id=%s;"


def report(start, end, district_id=None, courses=None, year=None, show_header=False):
    courses = get_course_ids(courses)

    if show_header:
        sys.stdout.write("district,school,user id,first name,last name,user name,email,cohort,registered date")
        
        for c in courses:
            sys.stdout.write(",course ID,registered,progress,pass,enrollment date")
            
        sys.stdout.write("\n")

    def user(user_id, username, district_id, cohort_id, first_name, last_name, email, school_id, activate_date):
        sys.stderr.write("Found user %s.\n" % email)

        user_courses = {}
        result = mysql_fetch_all(SQL_USER_COURSE % (user_id))

        for record in result:
            course_id = record[0]
            reg_date = record[1]
            if course_id in courses:
                user_courses[course_id] = {"reg_date": reg_date}

        sys.stdout.write('"%s","%s","%s","%s","%s","%s","%s","%s","%s"' %
                         (district_name(district_id), school_name(school_id), user_id,
                          first_name, last_name, username, email, cohort_code(cohort_id), activate_date))

        for cid in courses:
            c = user_courses.get(cid)
            p = 'Y' if c else 'N'
            reg_date = c["reg_date"] if c else ''
            scr = http_get_score(cid, username)
            if scr != 'E':
                pas = 'Y' if int(scr) >= 85 else 'N'
            else:
                pas = 'E'
            sys.stdout.write(',"%s","%s","%s%%","%s","%s"' % (cid, p, scr, pas, reg_date))

        sys.stdout.write("\n")
        sys.stdout.flush()

    cond = ""
    if district_id:
        cond += " and b.district_id=%s" % district_id

    if year:
        cond += " and year(b.activate_date)='%s'" % year

    result = mysql_fetch_all(SQL_USER % (cond, start-1, end-start+1))

    for u in result:
        user(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8])


def user_count(district_id=None, year=None):
    cond = ""
    if district_id:
        cond += " and b.district_id=%s" % district_id

    if year:
        cond += " and year(b.activate_date)='%s'" % year

    result = mysql_fetch_one(SQL_COUNT_USER % cond)
    print "user count:", result[0]


def course(courses=None):
    courses = get_course_ids(courses)
    for c in courses:
        print c


def http_get_score(course_id, username):
    score = ''
    import httplib
    import re
    httpClient = None
    try:
        httpClient = httplib.HTTPConnection('localhost', 8000, timeout=30)
        httpClient.request('GET', '/instructor/dashboard/progress/%s/%s' % (course_id, username))
        response = httpClient.getresponse()  # return a HTTPResponse object
        # print response.status
        # print response.reason
        content = response.read()
        m = re.search("progress:(\d+)", content)
        score = 'E' if not m else m.group(1)
    except Exception:
        score = "E"
    finally:
        if httpClient:
            httpClient.close()
    return score


def main(argv):
    # http://stackoverflow.com/questions/1492297/how-to-get-all-rows-starting-from-row-x-in-mysql
    cmd, district_id, s, e, courses = '', '', 1, 18446744073709551615, ''
    cmd = argv.pop(0)

    try:
        if cmd == 'count':
            opts, args = getopt.getopt(argv, "d:y:", ["district=", "year="])
        elif cmd == 'courses':
            opts, args = getopt.getopt(argv, "", [])
        elif cmd == 'report':
            opts, args = getopt.getopt(argv, "Hd:s:e:l:y:", ["district=", "start=", "end=", "lessions=", "header", "year="])
        elif cmd == '-h' or cmd == '--help':
            helping()
            exit(0)
        else:
            sys.stderr.write("invalid command. See ./course_users.py --help.\n")
            exit(2)
    except getopt.GetoptError:
        sys.stderr.write("invalid args. See ./course_users.py --help.\n")
        sys.exit(2)

    year, show_header = None, False

    for opt, arg in opts:
        if opt in ("-d", "--district"):
            district_id = arg
        elif opt in ("-s", "--start"):
            s = int(arg)
        elif opt in ("-e", "--end"):
            e = int(arg)
        elif opt in ("-y", "--year"):
            year = int(arg)
        elif opt in ("-H", "--header"):
            show_header = True
        elif opt in ("-l", "--lessions"):
            courses = arg

    if cmd == 'count':
        user_count(district_id, year)
    elif cmd == 'courses':
        course(courses)
    elif cmd == 'report':
        report(s, e, district_id, courses, year, show_header)


def helping():
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print """
  ******  Requirements:
  lms is running
  workon edx-platform
  cd ~/edx_all/scripts/utility

  ****** Usage:
  ./course_users.py command [options]

  ****** Args:
  command                       count:    total count of users selected
                                courses:  list course ids
                                report:   report learning status of users selected

  -l|--lessions=  course id (optional, for [report], quoted by '""', joined by ',')
  -d|--district=  district id (optional, for [count/report])
  -s|--start=     paging start (for [report])
  -e|--end=       paging end (for [report])
  -y|--year=      user joined year (for [count/report])
  -H|--header     print header (for [report])
  -h|--help       show this helping screen

  ****** Example:
  1) count of students
  ./course_users.py count
  ./course_users.py count -d 10

  2) list course ids
  ./course_users.py courses

  3) get study report
  ./course_users.py report -H
  ./course_users.py report -H -s 1 -e 2
  ./course_users.py report -H -d 10 -s 1 -e 2
  ./course_users.py report -H -d 10 -s 1 -e 2 -l \"WestEd/ELA101x/2014_Spring\"

  You can redirect report to csv, for example: ./course_users.py report -H > report.csv
        """

if __name__ == '__main__':
    main(sys.argv[1:])


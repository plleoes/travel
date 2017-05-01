# Create your views here.
from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils import translation
from contextlib import contextmanager
from pprint import pprint
from django.http import HttpResponse
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render
from googleapiclient.discovery import build
from djmail import template_mail
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import charset
import hashlib
import time
import datetime
import smtplib
import json
import uuid
import re

from travel.db import *
from travel.settings import *

class SomeTemplateEmail(template_mail.TemplateMail):
    name = "emailforget"

import os

@contextmanager
def language(lang):
    old_language = translation.get_language()
    try:
        translation.activate(lang)
        yield
    finally:
        translation.activate(old_language)



def my_view_index(request1):
    return render(request1,'Index.html')


def my_view_registrationta(request1):
    return render(request1,'RegistrationTA.html')


def my_view_registrationto(request1):
    return render(request1,'RegistrationTO.html')


def my_view_regto(request1):
    existsusers = False
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    tables = bqs.tables()
    tablesl = tables.list(projectId=PROYECT_ID,datasetId=DATASET_ID).execute()
    table_id = 'Users'
    table_ref = {'tableId': table_id,
                 'datasetId': DATASET_ID,
                 'projectId': PROYECT_ID}

    for t in tablesl['tables']:
        if t['tableReference']['tableId'] == table_id:
            existsusers=True
    if not existsusers:
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}
        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "UserCode"},
                {"type": "STRING", "name": "UserType"},
                {"type": "TIMESTAMP", "name": "Date"},
                {"type": "STRING", "name": "CompanyName"},
                {"type": "STRING", "name": "Address"},
                {"type": "STRING", "name": "City"},
                {"type": "STRING", "name": "State"},
                {"type": "STRING", "name": "Zip"},
                {"type": "STRING", "name": "Country"},
                {"type": "STRING", "name": "Phone"},
                {"type": "STRING", "name": "WebSite"},
                {"type": "STRING", "name": "Email"},
                {"type": "STRING", "name": "pwd"}
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()
    qr = bqs.jobs()
    qd = {
        'query': (
           'SELECT COUNT(*) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' + request1.POST.get('Email1TOn','') + '\"')
    }
    qres = qr.query(
        projectId=PROYECT_ID,
        body=qd).execute()


    if qres['rows'][0]['f'][0]['v'] == "0":
        start = time.time()
        job_id = 'job_%d' % start
        record = {'UserCode': hashlib.sha256(request1.POST.get('CompanyNameTOn','').encode('utf-8')+request1.POST.get('Email1TOn','').encode('utf-8')).hexdigest(),
                     'UserType': "Tour Operator",
                     'Date': time.time(),
                     'CompanyName': request1.POST.get('CompanyNameTOn',''),
                     'Address':  request1.POST.get('AddressTOn',''),
                     'City': request1.POST.get('CityTOn',''),
                     'State': request1.POST.get('StateTOn',''),
                     'Zip': request1.POST.get('ZipTOn',''),
                     'Country': request1.POST.get('CountryTOn',''),
                     'Phone': request1.POST.get('PhoneTOn',''),
                     'WebSite': request1.POST.get('WebSiteTOn',''),
                     'Email': request1.POST.get('Email1TOn',''),
                     'pwd': hashlib.sha256(request1.POST.get('Password1TOn','').encode('utf-8')).hexdigest()}

        irb = {
                 'rows': [
                     { 'json': record }
                  ]}

        ir = bqs.tabledata()
        ir.insertAll(projectId=PROYECT_ID,datasetId=DATASET_ID,tableId=table_id,body=irb).execute()


        return render(request1,'Index.html')
    else:
        return render(request1, 'Index.html',{'Error': _('User Already Registered') })


def my_view_regta(request1):
    existsusers = False
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    tables = bqs.tables()
    tablesl = tables.list(projectId=PROYECT_ID,datasetId=DATASET_ID).execute()
    table_id = 'Users'
    table_ref = {'tableId': table_id,
                 'datasetId': DATASET_ID,
                 'projectId': PROYECT_ID}

    for t in tablesl['tables']:
        if t['tableReference']['tableId'] == table_id:
            existsusers=True
    if not existsusers:
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}
        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "UserCode"},
                {"type": "STRING", "name": "UserType"},
                {"type": "TIMESTAMP", "name": "Date"},
                {"type": "STRING", "name": "CompanyName"},
                {"type": "STRING", "name": "Address"},
                {"type": "STRING", "name": "City"},
                {"type": "STRING", "name": "State"},
                {"type": "STRING", "name": "Zip"},
                {"type": "STRING", "name": "Country"},
                {"type": "STRING", "name": "Phone"},
                {"type": "STRING", "name": "WebSite"},
                {"type": "STRING", "name": "Email"},
                {"type": "STRING", "name": "pwd"}
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()
    qr = bqs.jobs()
    qd = {
        'query': (
           'SELECT COUNT(*) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' + request1.POST.get('Email1TAn','') + '\"')
    }
    qres = qr.query(
        projectId=PROYECT_ID,
        body=qd).execute()


    if qres['rows'][0]['f'][0]['v'] == "0":
        record = {'UserCode': hashlib.sha256(request1.POST.get('CompanyNameTAn','').encode('utf-8')+request1.POST.get('Email1TAn','').encode('utf-8')).hexdigest(),
                     'UserType': "Travel Agency",
                     'Date': time.time(),
                     'CompanyName': request1.POST.get('CompanyNameTAn',''),
                     'Address':  request1.POST.get('AddressTAn',''),
                     'City': request1.POST.get('CityTAn',''),
                     'State': request1.POST.get('StateTAn',''),
                     'Zip': request1.POST.get('ZipTAn',''),
                     'Country': request1.POST.get('CountryTAn',''),
                     'Phone': request1.POST.get('PhoneTAn',''),
                     'WebSite': request1.POST.get('WebSiteTAn',''),
                     'Email': request1.POST.get('Email1TAn',''),
                     'pwd': hashlib.sha256(request1.POST.get('Password1TAn','').encode('utf-8')).hexdigest()}

        irb = {
                 'rows': [
                     { 'json': record }
                  ]}

        ir = bqs.tabledata()
        ir.insertAll(projectId=PROYECT_ID,datasetId=DATASET_ID,tableId=table_id,body=irb).execute()


        return render(request1,'Index.html')
    else:
        return render(request1, 'Index.html',{'Error': _('User Already Registered') })

def my_view_webta(request1):
    credentials = GoogleCredentials.get_application_default()
    if request1.POST.get('EmailTA', '') != "" and request1.POST.get('PasswordTA','') != "":
        request1.session['EmailTA'] = request1.POST.get('EmailTA', '')
        request1.session['PasswordTA'] = hashlib.sha256(request1.POST.get('PasswordTA','').encode('utf-8')).hexdigest()



    bqs = build('bigquery', 'v2', credentials=credentials)
    table_id = 'Users'
    qr = bqs.jobs()
    qd = {
        'query': (
            'SELECT COUNT(*) FROM [' + DATASET_ID + '.' + table_id + '] WHERE UserType="Travel Agency" AND Email=\"' + request1.session['EmailTA'] + '\" AND pwd=\"' + request1.session['PasswordTA'] + '\" AND Date=(SELECT MAX(Date) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' +
            request1.session['EmailTA']
            + '\")')
    }
    qres = qr.query(
        projectId=PROYECT_ID,
        body=qd).execute()
    table_id2 = 'UserDefaultMargin'
    if qres['rows'][0]['f'][0]['v'] == "0":
        return render(request1, 'Index.html',{'Error': _('User or Password Failed') })
    else:
        existsuserdefaultm = False
        tables = bqs.tables()
        tablesl = tables.list(projectId=PROYECT_ID, datasetId=DATASET_ID).execute()
        for t in tablesl['tables']:
            if t['tableReference']['tableId'] == table_id2:
                existsuserdefaultm = True
        if not existsuserdefaultm:
            table_ref = {'tableId': table_id2,
                         'datasetId': DATASET_ID,
                         'projectId': PROYECT_ID}
            dataset_ref = {'datasetId': DATASET_ID,
                           'projectId': PROYECT_ID}
            schema_ref = {
                "fields": [
                    {"type": "STRING", "name": "UserCode"},
                    {"type": "TIMESTAMP", "name": "MDate"},
                    {"type": "FLOAT", "name": "Margin"},
                ]
            }
            table = {'tableReference': table_ref,
                     'schema': schema_ref}
            ttable = tables.insert(
                body=table, **dataset_ref).execute()

        qrn = bqs.jobs()
        qdn = {
            'query': (
                'SELECT CompanyName, UserCode FROM [' + DATASET_ID + '.' + table_id + '] WHERE UserType="Travel Agency" AND Email=\"' + request1.session['EmailTA'] + '\" AND pwd=\"' +request1.session['PasswordTA'] + '\" AND Date=(SELECT MAX(Date) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' + request1.session['EmailTA'] + '\" AND pwd=\"' + request1.session['PasswordTA']
                + '\")')
        }

        qresn = qrn.query(
            projectId=PROYECT_ID,
            body=qdn).execute()

        NameTA = qresn['rows'][0]['f'][0]['v']
        request1.session['NameTA'] = qresn['rows'][0]['f'][0]['v']
        request1.session['UserCode'] = qresn['rows'][0]['f'][1]['v']

        qrn3 = bqs.jobs()
        qdn3 = {
            'query': (
                'SELECT COUNT(*) FROM [' + DATASET_ID + '.' + table_id2 + '] WHERE UserCode=\"' +
                request1.session['UserCode'] + '\"')
        }
        qresn3 = qrn3.query(
            projectId=PROYECT_ID,
            body=qdn3).execute()
        if qresn3['rows'][0]['f'][0]['v'] == "0":
            return render(request1, 'DefaultMarginTA.html', {'NameTA': NameTA,  'Usr1': request1.session['UserCode']})
        else:
            return render(request1,'webTA.html', {'NameTA': NameTA})

def my_view_webto(request1):
    credentials = GoogleCredentials.get_application_default()
    if request1.POST.get('EmailTO', '') != "" and request1.POST.get('PasswordTO','') != "":
        request1.session['EmailTO'] = request1.POST.get('EmailTO', '')
        request1.session['PasswordTO'] = hashlib.sha256(request1.POST.get('PasswordTO','').encode('utf-8')).hexdigest()

    bqs = build('bigquery', 'v2', credentials=credentials)
    table_id = 'Users'
    qr = bqs.jobs()
    qd = {
        'query': (
            'SELECT COUNT(*) FROM [' + DATASET_ID + '.' + table_id + '] WHERE UserType="Tour Operator" AND Email=\"' + request1.session['EmailTO'] + '\" AND pwd=\"' + request1.session['PasswordTO'] + '\" AND Date=(SELECT MAX(Date) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' +
            request1.session['EmailTO']
            + '\")')
    }
    qres = qr.query(
        projectId=PROYECT_ID,
        body=qd).execute()
    table_id2 = 'UserCancelationPolicy'
    if qres['rows'][0]['f'][0]['v'] == "0":
        return render(request1, 'Index.html',{'Error': _('User or Password Failed') })
    else:
        existsusercancelation = False
        tables = bqs.tables()
        tablesl = tables.list(projectId=PROYECT_ID, datasetId=DATASET_ID).execute()
        for t in tablesl['tables']:
            if t['tableReference']['tableId'] == table_id2:
                existsusercancelation = True
        if not existsusercancelation:
            table_ref = {'tableId': table_id2,
                         'datasetId': DATASET_ID,
                         'projectId': PROYECT_ID}
            dataset_ref = {'datasetId': DATASET_ID,
                           'projectId': PROYECT_ID}
            schema_ref = {
                "fields": [
                    {"type": "STRING", "name": "UserCode"},
                    {"type": "TIMESTAMP", "name": "Date"},
                    {"type": "INTEGER", "name": "DaysBeforeDeparture"},
                    {"type": "FLOAT", "name": "ExpenditurePercentage"},
                    {"type": "BOOLEAN", "name": "IsMinimunExpense"},
                    {"type": "BOOLEAN", "name": "IsMoney"},
                    {"type": "BOOLEAN", "name": "Deleted"}
                ]
            }
            table = {'tableReference': table_ref,
                 'schema': schema_ref}
            ttable = tables.insert(
                body=table, **dataset_ref).execute()

        qrn2 = bqs.jobs()
        qdn2 = {
            'query': (
                'SELECT UserCode FROM [' + DATASET_ID + '.' + table_id + '] WHERE UserType="Tour Operator" AND Email=\"' + request1.session['EmailTO'] + '\" AND pwd=\"' +request1.session['PasswordTO'] + '\" AND Date=(SELECT MAX(Date) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' + request1.session['EmailTO'] + '\" AND pwd=\"' + request1.session['PasswordTO']
                + '\")')
        }
        qresn2 = qrn2.query(
            projectId=PROYECT_ID,
            body=qdn2).execute()
        request1.session['UserCode'] = qresn2['rows'][0]['f'][0]['v']

        qrn3 = bqs.jobs()
        qdn3 = {
            'query': (
                'SELECT COUNT(*) FROM [' + DATASET_ID + '.' + table_id2 + '] WHERE UserCode=\"' +
                request1.session['UserCode'] + '\"')
        }
        qresn3 = qrn3.query(
            projectId=PROYECT_ID,
            body=qdn3).execute()
        qrn = bqs.jobs()
        qdn = {
            'query': (
                'SELECT CompanyName FROM [' + DATASET_ID + '.' + table_id + '] WHERE UserType="Tour Operator" AND Email=\"' +
                request1.session['EmailTO'] + '\" AND pwd=\"' + request1.session[
                    'PasswordTO'] + '\" AND Date=(SELECT MAX(Date) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' +
                request1.session['EmailTO'] + '\" AND pwd=\"' + request1.session['PasswordTO']
                + '\")')
        }
        qresn = qrn.query(
            projectId=PROYECT_ID,
            body=qdn).execute()
        request1.session['NameTO'] = qresn['rows'][0]['f'][0]['v']
        NameTO = request1.session['NameTO']

        if qresn3['rows'][0]['f'][0]['v'] == "0":
            return render(request1, 'CancelationPolicyTO.html', {'NameTO': NameTO, 'Usr1': request1.session['UserCode']})
        else:



            return render(request1,'webTO.html', {'NameTO': NameTO, 'Uuid': uuid.uuid4()})

def my_view_forgetemail(request1):
    return render(request1,'EmailForget.html')

def my_view_up(request1):
    usr = request1.session['UserCode']
    NameTO = request1.session['NameTO']
    table_id1 = 'Travel'
    table_id2 = 'Excursions'
    table_id3 = 'Origins'
    table_id4 = 'TravelCancelationPolicy'
    table_id5 = 'Terms'
    table_id6 = 'TrendTerms'

    existtravel = False
    existexcursions = False
    existorigins = False
    existtravelcancelpolicy = False
    existterms = False
    existtrendterms = False
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    tables = bqs.tables()
    tablesl = tables.list(projectId=PROYECT_ID, datasetId=DATASET_ID).execute()
    for t in tablesl['tables']:
        if t['tableReference']['tableId'] == table_id1:
            existtravel = True
        if t['tableReference']['tableId'] == table_id2:
            existexcursions = True
        if t['tableReference']['tableId'] == table_id3:
            existorigins = True
        if t['tableReference']['tableId'] == table_id4:
            existtravelcancelpolicy = True
        if t['tableReference']['tableId'] == table_id5:
            existterms = True
        if t['tableReference']['tableId'] == table_id6:
            existtrendterms = True

    if not existtravel:
        table_ref = {'tableId': table_id1,
                     'datasetId': DATASET_ID,
                     'projectId': PROYECT_ID}
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}
        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "TravelCode"},
                {"type": "TIMESTAMP", "name": "TravelDate"},
                {"type": "STRING", "name": "UserCode"},
                {"type": "STRING", "name": "DestinatonRegion"},
                {"type": "STRING", "name": "DestinatonCountry"},
                {"type": "STRING", "name": "DestinatonZone"},
                {"type": "STRING", "name": "DestinatonEstate"},
                {"type": "STRING", "name": "DestinatonCity"},
                {"type": "STRING", "name": "Accommodation"},
                {"type": "RECORD", "name": "Words", "mode": "repeated",
                "fields": [{
                "name": "Word",
                "type": "STRING",
                "mode": "nullable"
                    }]
                },
                {"type": "TIMESTAMP", "name": "DateBegin"},
                {"type": "TIMESTAMP", "name": "DateEnd"},
                {"type": "RECORD", "name": "DepartureDays", "mode": "repeated",
                 "fields": [{
                     "name": "Month",
                     "type": "STRING",
                     "mode": "nullable"
                 }, {
                     "name": "Days",
                     "type": "STRING",
                     "mode": "nullable"
                 }]
                 },
                {"type": "INTEGER", "name": "PaxAvailable"},
                {"type": "INTEGER", "name": "NumberofTravelDays"},
                {"type": "FLOAT", "name": "PriceIndividualpax"},
                {"type": "FLOAT", "name": "Pricefor2pax"},
                {"type": "FLOAT", "name": "Priceperplus2pax"},
                {"type": "FLOAT", "name": "PerChildPrice"},
                {"type": "FLOAT", "name": "PerOneMoreDayIndividual"},
                {"type": "FLOAT", "name": "PerOneMoreDay2pax"},
                {"type": "FLOAT", "name": "PerOneMoreDayplus2pax"},
                {"type": "FLOAT", "name": "PerOneMoreDayChild"},
                {"type": "STRING", "name": "ContactEmail"},
                {"type": "STRING", "name": "ContactPhone"},
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()
    if not existexcursions:
        table_ref = {'tableId': table_id2,
                     'datasetId': DATASET_ID,
                     'projectId': PROYECT_ID}
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}

        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "ExTravelCode"},
                {"type": "STRING", "name": "ExcursionCode"},
                {"type": "TIMESTAMP", "name": "ExcursionDate"},
                {"type": "STRING", "name": "ExcursionDestination"},
                {"type": "INTEGER", "name": "NumberofDays"},
                {"type": "FLOAT", "name": "Priceperpax"},
                {"type": "FLOAT", "name": "PerChildPrice"}
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()
    if not existorigins:
        table_ref = {'tableId': table_id3,
                     'datasetId': DATASET_ID,
                     'projectId': PROYECT_ID}
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}

        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "OrTravelCode"},
                {"type": "STRING", "name": "OriginCode"},
                {"type": "TIMESTAMP", "name": "OriginDate"},
                {"type": "STRING", "name": "OriginCountry"},
                {"type": "STRING", "name": "OriginEstate"},
                {"type": "STRING", "name": "OriginCity"},
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()
    if not existtravelcancelpolicy:
        table_ref = {'tableId': table_id4,
                     'datasetId': DATASET_ID,
                     'projectId': PROYECT_ID}
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}

        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "CanpyTravelCode"},
                {"type": "STRING", "name": "CancelPolicyCode"},
                {"type": "TIMESTAMP", "name": "CancelPolicyDate"},
                {"type": "INTEGER", "name": "DaysBeforeDeparture"},
                {"type": "FLOAT", "name": "ExpenditurePercentage"},
                {"type": "BOOLEAN", "name": "IsMinimunExpense"},
                {"type": "BOOLEAN", "name": "IsMoney"},
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()
    if not existterms:
        table_ref = {'tableId': table_id5,
                     'datasetId': DATASET_ID,
                     'projectId': PROYECT_ID}
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}

        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "Term"}
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()
    if not existtrendterms:
        table_ref = {'tableId': table_id6,
                     'datasetId': DATASET_ID,
                     'projectId': PROYECT_ID}
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}

        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "TrendTerm"}
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()

    if request1.method == 'POST':
        temp_path = os.path.join(BASE_DIR, "tmp")
        if not request1.FILES:
            return render(request1, 'webTO.html', {'NameTO': NameTO, 'Uuid': uuid.uuid4(), 'Error': _('Must upload a file')})
        else:
            uid = request1.POST.get('Uuid', '')
            temp_path = os.path.join(temp_path, uid)
            file = request1.FILES["file"]
            if file.content_type !="application/octet-stream":
                os.rmdir(temp_path)
                return render(request1, 'webTO.html', {'NameTO': NameTO, 'Uuid': uuid.uuid4(), 'Error': _('Invalid file type')})
            else:
                if not os.path.exists(temp_path):
                    os.makedirs(temp_path)
                filename = os.path.join(temp_path, str(uuid.uuid4()) + file.name)
                destination = open(filename, "wb+")
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
                with open(filename, encoding='utf-8') as data_file:
                    try:
                        data = json.load(data_file)
                    except ValueError as e:
                        return render(request1, 'webTO.html', {'NameTO': NameTO, 'Uuid': uuid.uuid4(), 'Error': e})
                t1l = ["DestinatonRegion", "DestinatonCountry", "DestinatonZone", "DestinatonEstate", "DestinatonCity",
                       "Accommodation", "DateBegin", "DateEnd", "DepartureDays", "PaxAvailable", "NumberofTravelDays",
                       "PriceIndividualpax",
                       "Pricefor2pax", "Priceperplus2pax", "PerChildPrice", "PerOneMoreDayIndividual",
                       "PerOneMoreDay2pax",
                       "PerOneMoreDayplus2pax", "PerOneMoreDayChild", "ContactEmail", "ContactPhone"]
                t2l = ["ExcursionDestination", "NumberofDays", "Priceperpax", "PerChildPrice"]
                t3l = ["OriginCountry", "OriginEstate", "OriginCity"]
                t4l = ["DaysBeforeDeparture", "ExpenditurePercentage", "IsMinimunExpense", "IsMoney"]

                fieldlost = ""
                for row in data:
                    print(row)
                    for val in t1l:
                        if val not in row:
                            fieldlost+= val + " "
                    for d in row['Excursions']:
                        for v2 in t2l:
                            if val not in row:
                                fieldlost += val + " "
                    for d in row['Origins']:
                        for v2 in t3l:
                            if val not in row:
                                fieldlost += val + " "
                    for d in row['TravelCancelationPolicy']:
                        for v2 in t4l:
                            if val not in row:
                                fieldlost += val + " "
                if fieldlost != "":
                    os.remove(filename)
                    os.rmdir(temp_path)
                    return render(request1, 'webTO.html', {'NameTO': NameTO, 'Uuid': uuid.uuid4(), 'Error': "Missing Fields: " + fieldlost})
                excursions = []
                origins = []
                cancelpcy = []
                terms = []
                trendterms = []
                for i in range(len(data)):
                    tcode=str(uuid.uuid4())
                    data[i]['TravelCode'] = tcode
                    data[i]['TravelDate'] = str(time.time())
                    data[i]['UserCode'] = usr
                    data[i]['DateBegin'] = time.mktime(datetime.datetime.strptime(data[i]['DateBegin'],'%d/%m/%Y').timetuple())
                    data[i]['DateEnd'] = time.mktime(datetime.datetime.strptime(data[i]['DateEnd'], '%d/%m/%Y').timetuple())
                    data[i]['PaxAvailable'] = data[i].get('PaxAvailable','0')
                    data[i]['NumberofTravelDays'] = data[i].get('NumberofTravelDays','0')
                    data[i]['PriceIndividualpax'] = data[i].get('PriceIndividualpax','0')
                    data[i]['Pricefor2pax'] = data[i].get('Pricefor2pax','0')
                    data[i]['Priceperplus2pax'] = data[i].get('Priceperplus2pax','0')
                    data[i]['PerChildPrice'] = data[i].get('PerChildPrice','0')
                    data[i]['PerOneMoreDayIndividual'] = data[i].get('PerOneMoreDayIndividual','0')
                    data[i]['PerOneMoreDay2pax'] = data[i].get('PerOneMoreDay2pax','0')
                    data[i]['PerOneMoreDayplus2pax'] = data[i].get('PerOneMoreDayplus2pax','0')
                    data[i]['PerOneMoreDayChild'] = data[i].get('PerOneMoreDayChild','0')
                    comb = data[i].get('DestinatonRegion','').strip().lower() + " " + data[i].get('DestinatonCountry','').strip().lower() + " " + data[i].get('DestinatonZone','').strip().lower() \
                    + " " + data[i].get('DestinatonEstate','').strip().lower() + " " + data[i].get('DestinatonCity','').strip().lower() + " " + data[i].get('Accommodation','').strip().lower()
                    words = comb.split()
                    data[i]['Words'] = []
                    for z in range(len(words)):
                        data[i]['Words'].append({'Word': words[z]})

                    terms.append({'Term': data[i]['DestinatonRegion']})
                    terms.append({'Term': data[i]['DestinatonCountry']})
                    terms.append({'Term': data[i]['DestinatonZone']})
                    terms.append({'Term': data[i]['DestinatonEstate']})
                    terms.append({'Term': data[i]['DestinatonCity']})
                    trendterms.append({'TrendTerm': data[i]['DestinatonRegion']})
                    trendterms.append({'TrendTerm': data[i]['DestinatonCountry']})
                    trendterms.append({'TrendTerm': data[i]['DestinatonZone']})
                    trendterms.append({'TrendTerm': data[i]['DestinatonEstate']})
                    trendterms.append({'TrendTerm': data[i]['DestinatonCity']})

                    for n in range(len(data[i]['Excursions'])):
                        data[i]['Excursions'][n]['NumberofDays'] = data[i]['Excursions'][n].get('NumberofDays','0')
                        data[i]['Excursions'][n]['Priceperpax'] = data[i]['Excursions'][n].get('Priceperpax','0')
                        data[i]['Excursions'][n]['PerChildPrice'] = data[i]['Excursions'][n].get('PerChildPrice','0')
                        data[i]['Excursions'][n]['ExTravelCode'] = tcode
                        data[i]['Excursions'][n]['ExcursionCode'] = str(uuid.uuid4())
                        data[i]['Excursions'][n]['ExcursionDate'] = str(time.time())
                        excursions.append(data[i]['Excursions'][n])
                    for n in range(len(data[i]['Origins'])):
                        data[i]['Origins'][n]['OrTravelCode'] = tcode
                        data[i]['Origins'][n]['OriginCode'] = str(uuid.uuid4())
                        data[i]['Origins'][n]['OriginDate'] = str(time.time())
                        origins.append(data[i]['Origins'][n])
                    for n in range(len(data[i]['TravelCancelationPolicy'])):
                        data[i]['TravelCancelationPolicy'][n]['DaysBeforeDeparture'] = data[i]['TravelCancelationPolicy'][n].get('DaysBeforeDeparture','0')
                        data[i]['TravelCancelationPolicy'][n]['ExpenditurePercentage'] = data[i]['TravelCancelationPolicy'][n].get('ExpenditurePercentage','0')
                        data[i]['TravelCancelationPolicy'][n]['IsMinimunExpense'] = data[i]['TravelCancelationPolicy'][n].get('IsMinimunExpense','0')
                        data[i]['TravelCancelationPolicy'][n]['IsMoney'] = data[i]['TravelCancelationPolicy'][n].get('IsMoney','0')
                        data[i]['TravelCancelationPolicy'][n]['CanpyTravelCode'] = tcode
                        data[i]['TravelCancelationPolicy'][n]['CancelPolicyCode'] = str(uuid.uuid4())
                        data[i]['TravelCancelationPolicy'][n]['CancelPolicyDate'] = str(time.time())
                        cancelpcy.append(data[i]['TravelCancelationPolicy'][n])
                    del data[i]['Excursions']
                    del data[i]['Origins']
                    del data[i]['TravelCancelationPolicy']

                irb2 = "{'rows': ["
                for i in range(len(data)):
                    if i == len(data) - 1:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(data[i]) + "}"
                    else:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(data[i]) + "},"

                irb2 += "]}"
                irb2 = irb2.replace("'", "\"")
                irb = json.loads(irb2)
                pprint(irb)
                ir = bqs.tabledata()
                ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id1, body=irb).execute()
                irb2 = "{'rows': ["
                for i in range(len(excursions)):
                    if i == len(excursions) - 1:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(excursions[i]) + "}"
                    else:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(excursions[i]) + "},"

                irb2 += "]}"
                irb2 = irb2.replace("'", "\"")
                irb = json.loads(irb2)

                ir = bqs.tabledata()
                ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id2, body=irb).execute()
                irb2 = "{'rows': ["
                for i in range(len(origins)):
                    if i == len(origins) - 1:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(origins[i]) + "}"
                    else:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(origins[i]) + "},"

                irb2 += "]}"
                irb2 = irb2.replace("'", "\"")
                irb = json.loads(irb2)

                ir = bqs.tabledata()
                ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id3, body=irb).execute()
                irb2 = "{'rows': ["
                for i in range(len(cancelpcy)):
                    if i == len(cancelpcy) - 1:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(cancelpcy[i]) + "}"
                    else:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(cancelpcy[i]) + "},"

                irb2 += "]}"
                irb2 = irb2.replace("'", "\"")
                irb = json.loads(irb2)

                ir = bqs.tabledata()
                ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id4, body=irb).execute()
                irb2 = "{'rows': ["
                for i in range(len(terms)):
                    if i == len(terms) - 1:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(terms[i]) + "}"
                    else:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(terms[i]) + "},"

                irb2 += "]}"
                irb2 = irb2.replace("'", "\"")
                irb = json.loads(irb2)
                ir = bqs.tabledata()
                ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id5, body=irb).execute()

                irb2 = "{'rows': ["
                for i in range(len(trendterms)):
                    if i == len(trendterms) - 1:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(trendterms[i]) + "}"
                    else:
                        irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(trendterms[i]) + "},"

                irb2 += "]}"
                irb2 = irb2.replace("'", "\"")
                irb = json.loads(irb2)
                ir = bqs.tabledata()
                ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id6, body=irb).execute()
    else:
        return render(request1,'webTO.html', {'NameTO': NameTO, 'Uuid': uuid.uuid4(), 'Error': _('Unexpected Error')})

    os.remove(filename)
    os.rmdir(temp_path)
    return render(request1, 'webTO.html', {'NameTO': NameTO, 'Uuid': uuid.uuid4(), 'OK': _('Travel packages uploaded')})


def my_view_regcancelpolicy(request1):
    NameTO = request1.session['NameTO']
    table_id = 'UserCancelationPolicy'
    record = []
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    ismin = request1.POST.get('MinExpenses1n')
    ism = request1.POST.get('MoneyExpenses1n')

    if ismin == "true":
        isminstr="true"
    else:
        isminstr = "false"
    if ism == "true":
        ismstr="true"
    else:
        ismstr = "false"

    if request1.POST.get('CancelPyDaysn1n', '0') == "":
        daybe=-1
    else:
        daybe=request1.POST.get('CancelPyDaysn1n', '')
    if request1.POST.get('ExpensesPrctg1n', '0') == "":
        ex=0
    else:
        ex=request1.POST.get('ExpensesPrctg1n', '')


    record.append({'UserCode': request1.session['UserCode'],
              'Date': str(time.time()),
              'DaysBeforeDeparture': str(daybe),
              'ExpenditurePercentage': str(ex),
              'IsMinimunExpense': isminstr,
              'IsMoney': ismstr,
              'Deleted': "false"})
    daysb = request1.POST.getlist('CancelPyDaysnnl')
    exper = request1.POST.getlist('ExpensesPrctgnl')
    for i in range(len(daysb)):
        record.append({'UserCode': request1.session['UserCode'],
                     'Date': str(time.time()),
                     'DaysBeforeDeparture': daysb[i],
                     'ExpenditurePercentage': exper[i],
                     'IsMinimunExpense': 'false',
                     'IsMoney': 'false',
                     'Deleted': 'false'})

    irb2 = "{'rows': ["
    for i in range(len(record)):
        if i == len(record) - 1 :
            irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(record[i]) + "}"
        else:
            irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(record[i]) + "},"

    irb2+="]}"
    irb2=irb2.replace("'","\"")
    irb = json.loads(irb2)


    ir = bqs.tabledata()
    ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id, body=irb).execute()

    return render(request1, 'webTO.html', {'NameTO': NameTO, 'Uuid': uuid.uuid4(), 'Rclpy': record})

def my_view_regdefm(request1):
    NameTA = request1.session['NameTA']
    table_id = 'UserDefaultMargin'
    record = []
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    defmargin = request1.POST.get('DMarginn')
    record.append({'UserCode': request1.session['UserCode'],
              'MDate': str(time.time()),
              'Margin': defmargin})
    irb2 = "{'rows': ["
    for i in range(len(record)):
        if i == len(record) - 1 :
            irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(record[i]) + "}"
        else:
            irb2 += "{'insertId': '" + str(uuid.uuid4()) + "', 'json': " + str(record[i]) + "},"

    irb2+="]}"
    irb2=irb2.replace("'","\"")
    irb = json.loads(irb2)


    ir = bqs.tabledata()
    ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id, body=irb).execute()

    return render(request1, 'webTA.html', {'NameTA': NameTA, 'Uuid': uuid.uuid4(), 'MarginTA': defmargin})

def my_view_terms(request1):
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    table_id = 'Terms'
    qr = bqs.jobs()
    qd = {
        'query': (
            'SELECT Term FROM [' + DATASET_ID + '.' + table_id + '] GROUP BY Term ORDER BY Term ASC' )}
    qres = qr.query(
        projectId=PROYECT_ID,
        body=qd).execute()
    irb2 = "["
    for i in range(len(qres['rows'])):
        if i == len(qres['rows']) - 1:
            irb2 += "'" + qres['rows'][i]['f'][0]['v'] + "'"
        else:
            irb2 += "'" + qres['rows'][i]['f'][0]['v'] + "', "

    irb2 += "]"
    irb2 = irb2.replace("'", "\"")
    irb = json.loads(irb2)




    return HttpResponse(json.dumps(irb), content_type='application/json')

def my_view_tsearch(request1):
    text = request1.POST.get('text', '').lower()
    if text != "":
        t = text.replace(" ", ",")
        lo = len(t.split(","))


 
        credentials = GoogleCredentials.get_application_default()
        bqs = build('bigquery', 'v2', credentials=credentials)
        table_id1 = 'Travel'
        table_id2 = 'Users'
        table_id3 = 'Origins'
        table_id4 = 'Excursions'
        table_id5 = 'TravelCancelationPolicy'
        qr = bqs.jobs()
        #qd ={"query": ("SELECT Travels.TravelCode, Travels.DestinatonRegion, Travels.DestinatonCountry, Travels.DestinatonZone, Travels.DestinatonEstate, Travels.DestinatonCity, Travels.Accommodation, Travels.Combination, Users.CompanyName FROM ["+ DATASET_ID + "." + table_id1 + "] AS Travels JOIN [" + DATASET_ID + "." + table_id2 + "] AS Users ON Travels.UserCode = Users.UserCode WHERE Travels.TravelCode IN  (SELECT Travels2.TravelCode FROM ["+ DATASET_ID + "." + table_id1 + "] AS Travels2 WHERE Travels2.Words.Word IN (SELECT SPLIT(fragments) AS fragment FROM (SELECT '" + t + "' AS fragments)))")}
        qd ={"query": ("SELECT COUNT(Travels2.TravelCode) AS c, Travels2.TravelCode  FROM FLATTEN(["+ DATASET_ID + "." + table_id1 + "], Words) AS Travels2 JOIN FLATTEN((SELECT SPLIT(fragments) AS fragment FROM (SELECT '" + t + "' AS fragments)), fragment) AS w ON Travels2.Words.Word=w.fragment GROUP BY Travels2.TravelCode, Travels2.Pricefor2pax ORDER BY Travels2.Pricefor2pax LIMIT 100")}
        qres = qr.query(
            projectId=PROYECT_ID,
            body=qd).execute()
        print(qres)
        t2 = ""
        l = 0
        for i in range(len(qres['rows'])):
            if l < int(qres['rows'][i]['f'][0]['v']):
                l = int(qres['rows'][i]['f'][0]['v'])
        for i in range(len(qres['rows'])):
            if lo == int(qres['rows'][i]['f'][0]['v']):
                t2 += qres['rows'][i]['f'][1]['v'] + ","
            else:
                if l == int(qres['rows'][i]['f'][0]['v']):
                    t2 += qres['rows'][i]['f'][1]['v'] + ","

        t2 = t2[:-1]
        print(t2)
        qr = bqs.jobs()
        qd2 ={"flattenResults": False,
            "query": ("SELECT Travels.TravelCode, Travels.DestinatonRegion, Travels.DestinatonCountry, Travels.DestinatonZone, Travels.DestinatonEstate, Travels.DestinatonCity, Travels.Accommodation, Users.CompanyName, Travels.DateBegin, Travels.DateEnd, Travels.PaxAvailable, Travels.NumberofTravelDays, Travels.PriceIndividualpax, Travels.Pricefor2pax, Travels.Priceperplus2pax, Travels.PerChildPrice, Travels.PerOneMoreDayIndividual, Travels.PerOneMoreDay2pax, Travels.PerOneMoreDayplus2pax, Travels.PerOneMoreDayChild, Travels.ContactEmail, Travels.ContactPhone, GROUP_CONCAT(NEST(Travels.DepartureDays.Month)), GROUP_CONCAT(NEST(Travels.DepartureDays.Days)) FROM ["+ DATASET_ID + "." + table_id1 + "] AS Travels JOIN [" + DATASET_ID + "." + table_id2 + "] AS Users ON Travels.UserCode = Users.UserCode JOIN FLATTEN((SELECT SPLIT(fragments) AS fragment FROM (SELECT '" + t2 + "' AS fragments)), fragment) AS w ON Travels.TravelCode=w.fragment GROUP BY Travels.TravelCode, Travels.DestinatonRegion, Travels.DestinatonCountry, Travels.DestinatonZone, Travels.DestinatonEstate, Travels.DestinatonCity, Travels.Accommodation, Users.CompanyName, Travels.DateBegin, Travels.DateEnd, Travels.PaxAvailable, Travels.NumberofTravelDays, Travels.PriceIndividualpax, Travels.Pricefor2pax, Travels.Priceperplus2pax, Travels.PerChildPrice, Travels.PerOneMoreDayIndividual, Travels.PerOneMoreDay2pax, Travels.PerOneMoreDayplus2pax, Travels.PerOneMoreDayChild, Travels.ContactEmail, Travels.ContactPhone ORDER BY Travels.Pricefor2pax LIMIT 100")}
        qres2 = qr.query(
            projectId=PROYECT_ID,
            body=qd2).execute()
        qr = bqs.jobs()

        qd3 ={ "flattenResults": False,
            "query": ("SELECT OrTravelCode, OriginCountry, GROUP_CONCAT(NEST(OriginEstate)) AS OrEs, GROUP_CONCAT(NEST(OriginCity)) AS OrCy FROM ["+ DATASET_ID + "." + table_id3 + "] JOIN FLATTEN((SELECT SPLIT(fragments) AS fragment FROM (SELECT '" + t2 + "' AS fragments)), fragment) AS w ON OrTravelCode=w.fragment GROUP BY OrTravelCode, OriginCountry")}
        qres3 = qr.query(
            projectId=PROYECT_ID,
            body=qd3).execute()
        qr = bqs.jobs()
        qd4 ={ "flattenResults": False,
           "query": ("SELECT   ExTravelCode, GROUP_CONCAT(NEST(ExcursionDestination)) AS ExDes, GROUP_CONCAT(STRING(NEST(NumberofDays))) AS Ndays, GROUP_CONCAT(STRING(NEST(Priceperpax))) AS Price, GROUP_CONCAT(STRING(NEST(PerChildPrice))) AS Childprice FROM ["+ DATASET_ID + "." + table_id4 + "] JOIN FLATTEN((SELECT SPLIT(fragments) AS fragment FROM (SELECT '" + t2 + "' AS fragments)), fragment) AS w ON ExTravelCode=w.fragment GROUP BY ExTravelCode")}
        qres4 = qr.query(
            projectId=PROYECT_ID,
            body=qd4).execute()
        qr = bqs.jobs()
        qd5 ={ "flattenResults": False,
            "query": ("SELECT CanpyTravelCode, GROUP_CONCAT(STRING(NEST(DaysBeforeDeparture))) AS DaysB, GROUP_CONCAT(STRING(NEST(ExpenditurePercentage))) AS Expend, GROUP_CONCAT(NEST(CAST(IsMinimunExpense AS STRING))) AS IsMin, GROUP_CONCAT(NEST(CAST(IsMoney AS STRING))) AS IsMo FROM ["+ DATASET_ID + "." + table_id5 + "] JOIN FLATTEN((SELECT SPLIT(fragments) AS fragment FROM (SELECT '" + t2 + "' AS fragments)), fragment) AS w ON CanpyTravelCode=w.fragment GROUP BY CanpyTravelCode")}
        qres5 = qr.query(
            projectId=PROYECT_ID,
            body=qd5).execute()
        founded = []
        deptdays = []
        key = "rows"
        for y in range(len(qres2['rows'])):
            founded.append({'TravelCode': qres2['rows'][y]['f'][0]['v'],
                        'DestinationRegion': qres2['rows'][y]['f'][1]['v'],
                        'DestinationCountry': qres2['rows'][y]['f'][2]['v'],
                        'DestinationZone': qres2['rows'][y]['f'][3]['v'],
                        'DestinationEstate': qres2['rows'][y]['f'][4]['v'],
                        'DestinationCity': qres2['rows'][y]['f'][5]['v'],
                        'Accommodation': qres2['rows'][y]['f'][6]['v'],
                        'CompanyName': qres2['rows'][y]['f'][7]['v'],
                        'DateBegin': qres2['rows'][y]['f'][8]['v'],
                        'DateEnd': qres2['rows'][y]['f'][9]['v'],
                        'PaxAvailable': qres2['rows'][y]['f'][10]['v'],
                        'NumberofTravelDays': qres2['rows'][y]['f'][11]['v'],
                        'PriceIndividualpax': qres2['rows'][y]['f'][12]['v'],
                        'Pricefor2pax': qres2['rows'][y]['f'][13]['v'],
                        'Priceperplus2pax': qres2['rows'][y]['f'][14]['v'],
                        'PerChildPrice': qres2['rows'][y]['f'][15]['v'],
                        'PerOneMoreDayIndividual': qres2['rows'][y]['f'][16]['v'],
                        'PerOneMoreDay2pax': qres2['rows'][y]['f'][17]['v'],
                        'PerOneMoreDayplus2pax': qres2['rows'][y]['f'][18]['v'],
                        'PerOneMoreDayChild': qres2['rows'][y]['f'][19]['v'],
                        'ContactEmail': qres2['rows'][y]['f'][20]['v'],
                        'ContactPhone': qres2['rows'][y]['f'][21]['v']
                        })
            dates = []
            p = list(set(qres2['rows'][y]['f'][22]['v'].split(",")))
            lmes = qres2['rows'][y]['f'][22]['v'].split(",")
            tdays = []
            v = 0
            for valu in qres2['rows'][y]['f'][23]['v'].split('","'):
                tdays.append(valu.replace('"',''))
                year = datetime.datetime.fromtimestamp(float(qres2['rows'][y]['f'][8]['v'])).year
            for p in range(len(p)):
                lisd = tdays[p].split(",")
                for l in range(len(lisd)):
                    date = str(lisd[l]) + "/" + str(lmes[p]) + "/" + str(year)
                    dates.append(time.mktime(datetime.datetime.strptime(date, '%d/%m/%Y').timetuple()))
                    if lmes[p] == 12 and lmes[p+1] == 1:
                        year= year + 1
            origins = []
            if key in qres3:
                for z in range(len(qres3['rows'])):
                    if qres2['rows'][y]['f'][0]['v'] == qres3['rows'][z]['f'][0]['v']:
                        ors = qres3['rows'][z]['f'][3]['v'].split(",")
                        ors.sort()
                        for ori in ors:
                            origins.append({'OriginCity': ori})
            excursions = []
            if key in qres4:
                for z in range(len(qres4['rows'])):
                    if qres2['rows'][y]['f'][0]['v'] == qres4['rows'][z]['f'][0]['v']:
                        exdests = qres4['rows'][z]['f'][1]['v'].split(",")
                        nodaysa = qres4['rows'][z]['f'][2]['v'].split(",")
                        pricepexa = qres4['rows'][z]['f'][3]['v'].split(",")
                        pricechilda = qres4['rows'][z]['f'][4]['v'].split(",")
                        for f in range(len(exdests)):
                            excursions.append({'ExcursionDestination': exdests[f],
                                    'NumberofDays': int(nodaysa[f]),
                                    'Priceperpax': float(pricepexa[f]),
                                    'PerChildPrice': float(pricechilda[f])})
            tcancelpy = []
            if key in qres5:
                for z in range(len(qres5['rows'])):
                    if qres2['rows'][y]['f'][0]['v'] == qres5['rows'][z]['f'][0]['v']:
                        daysba = qres5['rows'][z]['f'][1]['v'].split(",")
                        expenda = qres5['rows'][z]['f'][2]['v'].split(",")
                        ismina = qres5['rows'][z]['f'][3]['v'].split(",")
                        ismoneya = qres5['rows'][z]['f'][4]['v'].split(",")
                        for f in range(len(daysba)):
                            excursions.append({'DaysBeforeDeparture': int(daysba[f]),
                                           'ExpenditurePercentage': float(expenda[f]),
                                           'IsMinimunExpense': bool(ismina[f]),
                                           'IsMoney': bool(ismoneya[f])})
            founded[y]['TDates'] = dates
            founded[y]['Origins'] = origins
            founded[y]['Excursions'] = excursions
            founded[y]['TravelCancelationPolicy'] = tcancelpy
    else:
        founded = ""


    return HttpResponse(json.dumps(founded), content_type='application/json')

def my_view_pack(request1):
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    table_id5 = 'Searches'
    table_id6 = 'Users'
    table_id7 = 'Terms'
    existsearches = False
    tables = bqs.tables()
    tablesl = tables.list(projectId=PROYECT_ID, datasetId=DATASET_ID).execute()
    for t in tablesl['tables']:
        if t['tableReference']['tableId'] == table_id5:
            existsearches = True
    if not existsearches:
        table_ref = {'tableId': table_id5,
                     'datasetId': DATASET_ID,
                     'projectId': PROYECT_ID}
        dataset_ref = {'datasetId': DATASET_ID,
                       'projectId': PROYECT_ID}

        schema_ref = {
            "fields": [
                {"type": "STRING", "name": "SearchCode"},
                {"type": "TIMESTAMP", "name": "Date"},
                {"type": "STRING", "name": "SearchCountry"},
                {"type": "STRING", "name": "SearchEstate"},
                {"type": "STRING", "name": "SearchCity"},
                {"type": "STRING", "name": "SearchZip"},
                {"type": "STRING", "name": "SearchString"}
            ]
        }
        table = {'tableReference': table_ref,
                 'schema': schema_ref}
        ttable = tables.insert(
            body=table, **dataset_ref).execute()
    qr = bqs.jobs()
    qd = {"query": (
    "SELECT City, State, Zip, Country FROM [" + DATASET_ID + "." + table_id6 + "] WHERE Email = '" + request1.session['EmailTA'] + "' LIMIT 100")}
    qres = qr.query(
        projectId=PROYECT_ID,
        body=qd).execute()
    searchor = []
    searchor.append({'SearchCode': str(uuid.uuid4()),
                     'Date': time.time(),
                     'SearchCity': qres['rows'][0]['f'][0]['v'],
                 'SearchEstate': qres['rows'][0]['f'][1]['v'],
                 'SearchZip': qres['rows'][0]['f'][2]['v'],
                 'SearchCountry': qres['rows'][0]['f'][3]['v'],
                 'SearchString': request1.POST.get('DestinationRegion', '') + " " + request1.POST.get('DestinatonCountry', '') + " " + request1.POST.get('DestinationZone', '') + " " + request1.POST.get('DestinatonEstate', '') + " " + request1.POST.get('DestinatonCity', '') + " " + request1.POST.get('Accommodation', '')
                 })
    irb = {
        'rows': [
            {'json': searchor}
        ]}


    ir = bqs.tabledata()
    ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id5, body=irb).execute()
    terms = []
    terms.append({'Term': request1.POST.get('Term', '')})
    irb = {
        'rows': [
            {'json': terms}
        ]}

    ir = bqs.tabledata()
    ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id7, body=irb).execute()
    data = []
    data.append({'Ok': True})

    return HttpResponse(json.dumps(data), content_type='application/json')



def my_view_rspd(request1):
    Usr1 = str(request1.GET.get('usrnur', ''))
    return render(request1,'Forget.html', {'Usr1': Usr1})

def my_view_forget(request1):
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    table_id = 'Users'
    qr = bqs.jobs()
    qd = {
        'query': (
            'SELECT COUNT(*) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' + request1.POST.get('Email1FPn', '') + '\"')
    }
    qres = qr.query(
        projectId=PROYECT_ID,
        body=qd).execute()

    if qres['rows'][0]['f'][0]['v'] == "0":
        return render(request1, 'Index.html', {'Error': _('User Not Registered')})
    else:
        tables = bqs.tables()
        tablesl = tables.list(projectId=PROYECT_ID, datasetId=DATASET_ID).execute()
        table_id2 = 'PwdChange'
        table_ref = {'tableId': table_id2,
                     'datasetId': DATASET_ID,
                     'projectId': PROYECT_ID}
        existsPwdChange=False
        for t in tablesl['tables']:
            if t['tableReference']['tableId'] == table_id2:
                existsPwdChange = True
        if not existsPwdChange:
            dataset_ref = {'datasetId': DATASET_ID,
                           'projectId': PROYECT_ID}
            schema_ref = {
                "fields": [
                    {"type": "STRING", "name": "UserCode"},
                    {"type": "TIMESTAMP", "name": "Date"},
                    {"type": "BOOLEAN", "name": "PwdChanged"},
                ]
            }
            table = {'tableReference': table_ref,
                     'schema': schema_ref}
            ttable = tables.insert(
                body=table, **dataset_ref).execute()
        qrm = bqs.jobs()
        qdm = {
            'query': (
                'SELECT LAST(UserCode) FROM [' + DATASET_ID + '.' + table_id + '] WHERE Email=\"' + request1.POST.get(
                    'Email1FPn', '') + '\"')
        }
        qresm = qrm.query(
            projectId=PROYECT_ID,
            body=qdm).execute()

        usr = qresm['rows'][0]['f'][0]['v']
        record = {'UserCode': usr,
                  'Date': time.time(),
                  'PwdChanged': "false"}

        irb = {
             'rows': [
                    {'json': record}
                ]}

        ir = bqs.tabledata()
        ir.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id2, body=irb).execute()
        qrme = bqs.jobs()
        qdme = {
             'query': (
                  'SELECT LAST(Email) FROM [' + DATASET_ID + '.' + table_id + '] WHERE UserCode=\"' + usr +'\"')
             }
        qresme = qrme.query(
            projectId=PROYECT_ID,
            body=qdme).execute()
        template_email = SomeTemplateEmail()
        emailto = str(qresme['rows'][0]['f'][0]['v'])
        lan = str(request1.LANGUAGE_CODE)
        with language(lan):
            email = template_email.make_email_object(emailto, {'name': _('Reset Password'),
                                                                'Usr': usr,
                                                               'Msg1': _('Email for Reset Password'),
                                                               'Msg2': _('For Reset Password click here'), "lang": lan})
            email.send()


        return render(request1,'Index.html', {'Error': _('Password reset email send')})

def my_view_upd(request1):
    credentials = GoogleCredentials.get_application_default()
    bqs = build('bigquery', 'v2', credentials=credentials)
    table_id = 'Users'
    table_id2 = 'PwdChange'
    qrme = bqs.jobs()
    qdme = {
        'query': (
            'SELECT PwdChanged FROM [' + DATASET_ID + '.' + table_id2 + '] WHERE UserCode=\"' + request1.POST.get('Usrn','') + '\" AND Date=(SELECT MAX(Date) FROM [' + DATASET_ID + '.' + table_id2 + '] WHERE UserCode=\"' + request1.POST.get('Usrn','')+ '\")')
    }
    qresme = qrme.query(
        projectId=PROYECT_ID,
        body=qdme).execute()

    if qresme['rows'][0]['f'][0]['v'] != "true":
        qrm = bqs.jobs()
        qdm = {
            'query': (
                'SELECT * FROM [' + DATASET_ID + '.' + table_id + '] WHERE UserCode=\"' + request1.POST.get('Usrn','') + '\" AND Date=(SELECT MAX(Date) FROM [' + DATASET_ID + '.' + table_id + '] WHERE UserCode=\"' + request1.POST.get('Usrn','')
                + '\")')
        }
        qresm = qrm.query(
            projectId=PROYECT_ID,
            body=qdm).execute()
        record = {'UserCode': qresm['rows'][0]['f'][0]['v'],
              'UserType': qresm['rows'][0]['f'][1]['v'],
              'Date': time.time(),
              'CompanyName': qresm['rows'][0]['f'][3]['v'],
              'Address': qresm['rows'][0]['f'][4]['v'],
              'City': qresm['rows'][0]['f'][5]['v'],
              'State': qresm['rows'][0]['f'][6]['v'],
              'Zip': qresm['rows'][0]['f'][7]['v'],
              'Country': qresm['rows'][0]['f'][8]['v'],
              'Phone': qresm['rows'][0]['f'][9]['v'],
              'WebSite': qresm['rows'][0]['f'][10]['v'],
              'Email': qresm['rows'][0]['f'][11]['v'],
              'pwd': hashlib.sha256(request1.POST.get('Password1TAn', '').encode('utf-8')).hexdigest()}

        table_id2 = 'PwdChange'
        irb = {
        'rows': [
            {'json': record}
            ]}
        ira = bqs.tabledata()
        ira.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id, body=irb).execute()

        recordb = {'UserCode': request1.POST.get('Usrn',''),
              'Date': time.time(),
              'PwdChanged': "true"}


        ird = {
            'rows': [
            {'json': recordb}
            ]}


        irc = bqs.tabledata()
        irc.insertAll(projectId=PROYECT_ID, datasetId=DATASET_ID, tableId=table_id2, body=ird).execute()
        return render(request1, 'Index.html')
    else:
        return render(request1, 'Index.html', {'Error': _('Password already reset')})

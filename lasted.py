#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TypeDecorator, Unicode
from xdb import Base, User, Sheet, History, Suppliers, Item
from flask import session as login_session
import random
import string
import excel
import httplib2
import json
from flask import make_response
import requests
import pandas as pd
from tablib import Dataset
import numpy as np
import excel
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import xlsxwriter
import pyarabic.araby as araby
import pyarabic.number as number
import arabic_reshaper
from bidi.algorithm import get_display
import sys
from sqlalchemy import func

reload(sys)  
sys.setdefaultencoding('utf-8')
engine = create_engine('sqlite:///x.db')
Base.metadata.bind = engine
engine.text_factory = str

DBSession = sessionmaker(bind=engine)
session = DBSession()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['xls', 'xlsb', 'xlsm', 'xlsx', 'xlt', 'xltx', 'xlw', 'csv'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




class CoerceUTF8(TypeDecorator):
    """Safely coerce Python bytestrings to Unicode
    before passing off to the database."""

    impl = Unicode

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            value = value.decode('utf-8')
        return value


@app.route('/sheet/JSON')
def sheetJSON():
    sheet = session.query(Sheet).all()
    return jsonify(Request=[r.serialize for r in sheet])



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    sheets = session.query(Sheet).all()
    sheet_count = int(len(sheets))
    numbers = 1
    if sheet_count == 0:
        sheet_count = u"لا توجد طلبات"
        numbers = 0
    return render_template('index.html', sheets_number=sheet_count, numbers=numbers)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'form2' in request.form:
            if request.form['request_date'] != '':
                man_request_date = request.form['request_date']
            else:
                man_request_date = "-"              

            if request.form['item_name'] != '':
                man_item_name = request.form['item_name']
            else:
                man_item_name = "-"    

            if request.form['description'] != '':
                man_description = request.form['description']
            else:
                man_description = "-"    

            if request.form['project'] != '':
                man_project = request.form['project']
            else:
                man_project = "-"    

            if request.form['manufacturing_order'] != '':
                man_manufacturing_order = request.form['manufacturing_order']
            else:
                man_manufacturing_order = "-"    

            if request.form['order_number'] != '':
                man_order_number = request.form['order_number']
            else:
                man_order_number = "-"    

            if request.form['pr'] != '':
                man_pr = request.form['pr']
            else:
                man_pr = "-"    

            if request.form['unit'] != '':
                man_unit = request.form['unit']
            else:
                man_unit = "-"    

            if request.form['quantity_to_buy'] != '':
                man_quantity_to_buy = request.form['quantity_to_buy']
            else:
                man_quantity_to_buy = "-"    

            if request.form['accepted'] != '':
                man_accepted = request.form['accepted']
            else:
                man_accepted = "-"    

            if request.form['remaining'] != '':
                man_remaining = request.form['remaining']
            else:
                man_remaining = "-"    

            if request.form['delivery_date'] != '':
                man_delivery_date = request.form['delivery_date']
            else:
                man_delivery_date = "-"    

            if request.form['supplier'] != '':
                man_supplier = request.form['supplier']
            else:
                man_supplier = "-"    

            if request.form['delivery_order_number'] != '':
                man_delivery_order_number = request.form['delivery_order_number']
            else:
                man_delivery_order_number = "-"    

            if request.form['notes'] != '':
                man_notes = request.form['notes']
            else:
                man_notes = "-"

            new_row = Sheet(request_date=man_request_date, item_name=man_item_name,
                            description=man_description,project=man_project, manufacturing_order=man_manufacturing_order,
                            order_number=man_order_number,pr=man_pr, unit=man_unit,
                            quantity_to_buy=man_quantity_to_buy,accepted=man_accepted,
                            remaining=man_remaining, delivery_date=man_delivery_date,supplier=man_supplier,
                            delivery_order_number=man_delivery_order_number, notes=man_notes)
             
            #ar_request_date = request.form['request_date']
            #ar_item_name = request.form['request_date']
            #ar_description = request.form['request_date']
            #ar_project = request.form['request_date']
            #ar_manufacturing_order = request.form['request_date']
            #ar_order_number = request.form['request_date']
            #ar_pr = request.form['request_date']
            #ar_unit = request.form['request_date']
            #ar_quantity_to_buy = request.form['request_date']
            #ar_accepted = request.form['request_date']
            #ar_remaining = request.form['request_date']
            #ar_delivery_date = request.form['request_date']
            #ar_supplier = request.form['request_date']
            #ar_delivery_order_number = request.form['request_date']
            #ar_notes = request.form['request_date']


	
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file_path = UPLOAD_FOLDER + "/" + filename
            nx = pd.read_excel(file_path, charset='utf-8')
            lf = pd.DataFrame(nx)

            table_names = []
			# this to use arbaic and arabic libr 
            ar_request_date = u'تاريخ الطلب'
            ar_item_name = u'اسم الصنف'
            ar_description = u'المواصفات'
            ar_project = u'اسم العميل/المشروع'            
            ar_manufacturing_order = u'امر التصنيع'
            ar_order_number = u'رقم طلب المشتريات'
            ar_pr = u'pr'
            ar_unit = u'الوحدة'
            ar_quantity_to_buy = u'الكمية المطلوب شرائها'
            ar_accepted = u'الكمية المقبولة'
            ar_remaining = u'الكمية المتبقية'
            ar_delivery_date = u'تاريخ التسليم الفعلي'
            ar_supplier = u'اسم المورد'
            ar_delivery_order_number = u'رقم اذن التسليم'
            ar_notes = u'ملحظات'            
            # store all headers (columns) in one list 
            sheet_headers = [ar_request_date, ar_item_name, ar_description,
                             ar_project, ar_manufacturing_order, ar_order_number,
                             ar_pr, ar_unit, ar_quantity_to_buy, ar_accepted,
                             ar_remaining, ar_delivery_date, ar_supplier,
                             ar_delivery_order_number, ar_notes]
            #ar_request_date
            ar_item_name.encode('utf8')
            ar_description.encode('utf8')
            ar_project.encode('utf8')
            ar_manufacturing_order.encode('utf8')
            ar_order_number.encode('utf8')
            ar_pr.encode('utf8')
            ar_unit.encode('utf8')
            ar_quantity_to_buy.encode('utf8')
            ar_accepted.encode('utf8')
            ar_remaining.encode('utf8')
            ar_delivery_date.encode('utf8')
            ar_supplier.encode('utf8')
            ar_delivery_order_number.encode('utf8')
            ar_notes.encode('utf8')
            
            df = pd.DataFrame(nx, columns= sheet_headers)

            request_dates = []
            item_names = []
            descriptions = []
            projects = []
            manufacturing_orders = []
            order_numbers = []
            prs = []
            units = []
            quantitys_to_buys = []
            accepteds = []
            remainings = []
            delivery_dates = []
            suppliers = []
            delivery_orders_numbers = []
            notess = []

            #bidi_text.encode('utf8')
            for r_date in df[ar_request_date]:
                request_dates.append(str(r_date))
                print(r_date)
                
            for r_name in df[ar_item_name]:
                item_names.append(r_name)
                
            for r_description in df[ar_description]: 
                descriptions.append(r_description)
                
            for r_projet in df[ar_project]:
                projects.append(r_projet)
                
            for r_manufacturing in df[ar_manufacturing_order]:
                manufacturing_orders.append(r_manufacturing)
                
            for r_ordernumber in df[ar_order_number]:
                order_numbers.append(r_ordernumber)
                
            for r_pr in df[ar_pr]:
                prs.append(r_pr)
                
            for r_unit in df[ar_unit]:
                units.append(r_unit)
                
            for r_bquantity in df[ar_quantity_to_buy]:
                quantitys_to_buys.append(r_bquantity)
                
            for r_accepted in df[ar_accepted]:
                accepteds.append(r_accepted)
                
            for r_remaining in df[ar_remaining]:
                remainings.append(r_remaining)
                
            for r_delivery_date in df[ar_delivery_date]:
                delivery_dates.append(r_delivery_date)
                
            for r_supplier in df[ar_supplier]:
                suppliers.append(r_supplier)
                
            for r_deliver_orders in df[ar_delivery_order_number]:
                delivery_orders_numbers.append(r_deliver_orders)
                
            for r_notes in df[ar_notes]:
                notess.append(r_notes)                
            print(len(item_names))
            for row in range(len(item_names)):
                ju_request_dates = request_dates[row]
                ju_item_names = item_names[row]
                ju_descriptions = descriptions[row]
                ju_projects = projects[row]
                ju_manufacturing_orders = manufacturing_orders[row]
                ju_order_numbers = order_numbers[row]
                ju_prs = prs[row]
                ju_units = units[row]
                ju_quantitys_to_buys = quantitys_to_buys[row]
                ju_accepteds = accepteds[row]
                ju_remainings = remainings[row]
                ju_delivery_dates = delivery_dates[row]
                ju_suppliers = suppliers[row]
                ju_delivery_orders_numbers = delivery_orders_numbers[row]
                ju_notess = notess[row]
                new_row = Sheet(request_date=ju_request_dates, item_name=ju_item_names, description=ju_descriptions,
                                project=ju_projects, manufacturing_order=ju_manufacturing_orders, order_number=ju_order_numbers,
                                pr=ju_prs, unit=ju_units, quantity_to_buy=ju_quantitys_to_buys,
                                accepted=ju_accepteds, remaining=ju_remainings, delivery_date=ju_delivery_dates,
                                supplier=ju_suppliers, delivery_order_number=ju_delivery_orders_numbers, notes=ju_notess)
                session.add(new_row)
            session.commit()            
            flash('Successfully Added Request : %s ' % new_row.pr)
            sheets = session.query(Sheet).order_by(asc(Sheet.id)).all()
            
            return redirect(url_for('i_request_Function', sheets=sheets))
            
            print("GoodJob Robot %s" % new_row.request_date)

    
        
    return render_template('pages/forms/i_general.html')
    #sheets_number = len(session.query(Sheet).order_by(asc(Sheet.id)).all())
    #return render_template('pages/forms/i_general.html', sheets=sheets, sheets_number=sheets_number)






@app.route('/i_request')
def i_request_Function():
    sheets = session.query(Sheet).order_by(asc(Sheet.id)).all()
    return render_template('/pages/tables/internal_request.html', sheets=sheets)

@app.route('/is_request')
def is_request_Function():
    suppliers = session.query(Suppliers).order_by(asc(Suppliers.id)).all()
    sheets = session.query(Sheet).all()
    sheets_number = len(sheets)
    return render_template('/pages/tables/internal_supplier_request.html', suppliers=suppliers, sheets_number=sheets_number)


@app.route('/i_general', methods = ['GET'])
def ilovepython():
    return render_template('/pages/forms/internal_form.html')
 

@app.route('/is_general', methods = ['GET'])
def i_s_general():
    return render_template('/pages/forms/internal_supplier_form.html')
 





@app.route('/e_request')
def e_request_Function():
    sheets = session.query(Sheet).order_by(asc(Sheet.id)).all()
    return render_template('/pages/tables/external_request.html', sheets=sheets)

@app.route('/es_request')
def es_request_Function():
    suppliers = session.query(Suppliers).order_by(asc(Suppliers.id)).all()
    sheets = session.query(Sheet).all()
    sheets_number = len(sheets)
    return render_template('/pages/tables/external_supplier_request.html', suppliers=suppliers, sheets_number=sheets_number)


@app.route('/e_general', methods = ['GET'])
def e_general():
    return render_template('/pages/forms/external_form.html')
 

@app.route('/es_general', methods = ['GET'])
def e_s_general():
    return render_template('/pages/forms/external_supplier_form.html')
 



    
@app.route('/home/<int:sheet_id>' , methods=['GET', 'POST'])
def getSheet(sheet_id):
    sheet = session.query(Sheet).filter_by(id=sheet_id).first()
    page = "<style>table {width:100%;}table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {  padding: 15px;text-align: left;}#t01 tr:nth-child(even) {background-color: #eee;}#t01 tr:nth-child(odd) {background-color: #fff;}#t01 th { background-color: black;color: white;}</style>"
    page += "<table><tr><th>Name</th><th>Age</th><th>Gender</th><th>phone</th><th>count</th></tr><tr>"
    page += "<td>" + str(sheet.name) + "</td>" +  "<td>" + str(sheet.pr) + "</td>" + "<td>" + str(sheet.date) + "</td>"
    page += "<td>" + str(sheet.supplier) + "</td>" + "<td>" + str(sheet.quait) + "</td></tr></table>"
    return page


@app.route('/home/all' , methods=['GET'])
def getAll():
    sheet = session.query(Sheet).all()
    page = "<style>table {width:100%;}table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {  padding: 15px;text-align: left;}#t01 tr:nth-child(even) {background-color: #eee;}#t01 tr:nth-child(odd) {background-color: #fff;}#t01 th { background-color: black;color: white;}</style>"
    page += "<table><tr><th>Name</th><th>Age</th><th>Gender</th><th>phone</th><th>count</th></tr><tr>"
    for i in sheet:
        page += "<td>" + str(i.name) + "</td>" +  "<td>" + str(i.pr) + "</td>" + "<td>" + str(i.date) + "</td>"
        page += "<td>" + str(i.supplier) + "</td>" + "<td>" + str(i.quait) + "</td></tr>"
    page += "</table>"    
    return page

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080, threaded=False)



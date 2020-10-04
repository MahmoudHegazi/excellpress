# excellpress
Upload any Excel Sheet, Using ML the app can upload the excel sheet and recognize the headers name and create columns with flexbox, store your data in database to check them later, also you can control how your excl sheet web version look like, finally you can download. soon I'm going to add another step to convert your new excel to web sheet to pdf  

#why this app
becuase it's very fast, you will see your huge excelsheet in short time shorter  google search result ..!!! clone it and check by yourself

send mobile message python (easy steps)
https://2wenosco.odoo.com/web#action=163&model=mailing.mailing&view_type=kanban&cids=1&menu_id=120

vagrant
2.2.7

vbox
5.2.38
```python
app.config['JSON_AS_ASCII'] = False
```

https://stackoverflow.com/questions/60239099/csv-file-with-arabic-characters-is-displayed-as-symbols-in-excel
UnicodeDecodeError: 'ascii' codec can't decode byte 0xd8 in position 0: ordinal not in range(128)

https://pypi.org/project/PyArabic/


```python
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from xdb import Base, User, Sheet, History 
from flask import session as login_session
import random
import string
import excel
# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
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

engine = create_engine('sqlite:///x.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['xls', 'xlsb', 'xlsm', 'xlsx', 'xlt', 'xltx', 'xlw', 'csv'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/sheet/JSON')
def sheetJSON():
    sheet = session.query(Sheet).all()
    return jsonify(Request=[r.serialize for r in sheet])



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
	
        
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
            nx = pd.read_excel(file_path)
            lf = pd.DataFrame(nx)

            table_names = []
            text = u'الأسم'
            nxon = text.encode('utf8')
                
            df = pd.DataFrame(nx, columns= ['الأسم', 'P Number', 'Dore', 'Supplier','الأسم'])
            #writer = pd.ExcelWriter(nx, engine='xlsxwriter')
            #df.to_excel(writer, sheet_name='Sheet1', encoding="utf-8-sig")
            #writer.save()		
			
            names = []
            prs = []
            dates = []
            suppliers = []
            quants = []
            
            for xname in df['الأسم']:
                names.append(xname)
                print(xname)
            for xpnumber in df['P Number']:
                prs.append(xpnumber)
            for xdate in df['Dore']:
                dates.append(xdate)
            for xsupplier in df['Supplier']:
                suppliers.append(xsupplier)            
            for xquant in df['الأسم']:
                quants.append(xquant)

            for row in range(len(names)):
                ju_name = u'names[row]'
                ju_pnumber = prs[row]
                ju_date = dates[row]
                ju_supplier = suppliers[row]
                ju_quait = quants[row]
                new_row = Sheet(name=ju_name, pr=ju_pnumber, date=ju_date, supplier=ju_supplier, quait=ju_quait)
                session.add(new_row)
            session.commit()
            
            print("GoodJob Robot %s" % new_row.name)


    return render_template('index.html')

@app.route('/home/<int:sheet_id>' , methods=['GET', 'POST'])
def getSheet(sheet_id):
    sheet = session.query(Sheet).filter_by(id=sheet_id).first()
    return str(sheet.pr)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080, threaded=False)




```

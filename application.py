#https://harshini7780assm2.azurewebsites.net/

from flask import Flask,redirect,render_template,request
import pyodbc
import datetime
from datetime import date, datetime, time


app=Flask(__name__)
@app.route('/')
def home():
    msg = pyodbc.drivers()
    
    return render_template("home.html", msg=msg)
#Search for and count all earthquakes that occurred with a magnitude greater  than 5.0
@app.route("/largest",methods=["POST","GET"])
def largest():
    cnxn=pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:harshinibigdata.database.windows.net,1433;Database=harshini;Uid=harshini7780;Pwd=MADHUbala.123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor=cnxn.cursor()   
    cursor.execute("SELECT COUNT(*) FROM dbo.significant_month WHERE mag > 5.0;")
    rows = cursor.fetchall() 
    result = []
    for r in rows:
        result.append(r)
    # cursor.connection.commit()
    return render_template('largest.html', result=result)
#ind earthquakes that were near (20 km, 50 km?) of a specified location. 
@app.route('/range',methods=['GET','POST'])
def specifiedLocation():
    if(request.method=='POST'):
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        radius = float(request.form['radius'])/111.12
        print(latitude,radius)
        cnxn=pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:harshinibigdata.database.windows.net,1433;Database=harshini;Uid=harshini7780;Pwd=MADHUbala.123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    
        cursor=cnxn.cursor()
        query="select * from significant_month where  latitude >= ? and latitude <= ? and longitude >= ? and longitude <=?"
        parameters=(latitude-radius,latitude+radius,longitude-radius,longitude+radius)
        results=cursor.execute(query,parameters)
        rows = cursor.fetchall()
        cnxn.close()
        print(rows)
        return render_template("range_basic.html",rows = rows) 
    return render_template("range.html") 


@app.route("/q3_m",methods=["POST","GET"])
def q3():
    if(request.method=='POST'):
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        radius = float(request.form['radius'])/111.12
        cnxn=pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:harshinibigdata.database.windows.net,1433;Database=harshini;Uid=harshini7780;Pwd=MADHUbala.123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor=cnxn.cursor()
        query='''select * from significant_month where latitude >= ? and latitude <= ? and longitude >= ? and longitude <=? and type = 'earthquake' and (select count(*) from significant_month WHERE latitude >= ? and latitude <= ? and (longitude >= ? and longitude <= ?)and type = 'earthquake') >4'''
        parameters=(latitude-radius,latitude+radius,longitude-radius,longitude+radius,latitude-radius,latitude+radius,longitude-radius,longitude+radius)
        results=cursor.execute(query,parameters)               
        rows=cursor.fetchall()
        result=[]
        for r in rows:
            result.append(r)
        print(result)
    #cursor.connection.commit()
        return render_template('q3.html',result=result)
    return render_template('q3_m.html')
#Search for 2.0 to 2.5, 2.5 to 3.0, etc magnitude quakes for a one week, a range of days or the whole 30 days.
@app.route("/q4", methods=["POST","GET"])
def q4():
    cnxn=pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:harshinibigdata.database.windows.net,1433;Database=harshini;Uid=harshini7780;Pwd=MADHUbala.123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor=cnxn.cursor()
    cursor.execute('''select two, three,three_half, four, four_half, five,five_half,six,six_half,seven,seven_half,eight 
    from (select count(*) as two from significant_month where mag between 2 and 2.5 ) as two,
(select count(*) as three from significant_month where mag between 2.5 and 3 ) as three,
(select count(*) as three_half from significant_month where mag between 3 and 3.5 ) as three_half,
(select count(*) as four from significant_month where mag between 3.5 and 4 ) as four,
(select count(*) as four_half from significant_month where mag between 4 and 4.5) as four_half,
(select count(*) as five from significant_month where mag between 4.5 and 5 ) as five,

(select count(*) as five_half from significant_month where mag between 5 and 5.5 ) as five_half,
(select count(*) as six from significant_month where mag between 5.5 and 6) as six,
(select count(*) as six_half from significant_month where mag between 6 and 6.5) as six_half,
(select count(*) as seven from significant_month where mag between 6.5 and 7 ) as seven,
(select count(*) as seven_half from significant_month where mag between 7 and 7.5 ) as seven_half,
(select count(*) as eight from significant_month where mag between 7.5 and 8 ) as eight''')

    rows=cursor.fetchall()
    result=[]
    for r in rows:
        result.append(r)
    return render_template("q4.html",result=result)

@app.route('/q5',methods=["POST","GET"])
def q5():
    cnxn=pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:harshinibigdata.database.windows.net,1433;Database=harshini;Uid=harshini7780;Pwd=MADHUbala.123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor=cnxn.cursor()
    cursor.execute('''SELECT time from significant_month;''')
    rows=cursor.fetchall()
    h=[]
    for s in rows:
        dt = datetime.strptime(s[0], "%Y-%m-%dT%H:%M:%S.%f%z")
        time = dt.time()
        hour = time.strftime('%H')
        h.append(hour)
    print(h)    
    day=0
    night=0    
    for i in h:  
        if int(i)>=6 and int(i)<18:
            day=day+1
        else:
            night=night+1
    result=[]
    result.append(day)
    result.append(night)
    return render_template("q5.html",result=[day,night])



if __name__=='__main__':
    app.run(debug=True)
# MRUTYUNJAYSINH VAGHELA-1002078423
# DARSHIL SHAH-1002084331 
from flask import Flask, render_template, request, redirect,url_for
import mysql.connector

app = Flask(__name__)

#connection to Mysql database
conn = con = mysql.connector.connect(host='academicmysql.mysql.database.azure.com',
                              database='djs4331',
                              user='djs4331',
                              password='Darshil2107')
cur = conn.cursor()

# view customer
@app.route('/', methods=['GET', 'POST'])
def index():
    select_records = ("SELECT * FROM CAR")
    cur.execute(select_records)
    records = cur.fetchall()
    return render_template('index.html', records=records)

# add customer
@app.route('/add_customer', methods=['GET','POST'])
def add_customer():
    # get form data
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_no = request.form['contact_no']
        customer_type = request.form['customer_type']

        cursor = conn.cursor()
    
    # insert new customer data into database
        add_customer_query = ("INSERT INTO CUSTOMER (F_NAME, L_NAME, CONTACT_NO, C_TYPE) "
                          "VALUES (%s, %s, %s, %s)")
        customer_data = (first_name, last_name, contact_no, customer_type)
        cursor.execute(add_customer_query, customer_data)
        conn.commit()
        return redirect('/')
    else:
    # redirect to success page
      return render_template('addcustomer.html')

#add car
@app.route('/add_car', methods=['GET','POST'])
def add_car():
    # get form data
    if request.method=='POST':
        model = request.form['model']
        year = request.form['year']
        category = request.form['category']
        Daily_Rate = request.form['Daily_Rate']
        Weekly_Rate = request.form['Weekly_Rate']
        Available = request.form['Available']
        car_type = request.form['car_type']
        own_id = request.form['own_id']
        cursor = conn.cursor()
    
    # insert new customer data into database
        add_customer_query = ("INSERT INTO CAR (MODEL, YEAR, CATEGORY, DAILY_RATE, WEEKLY_RATE, AVAILABLE, CAR_TYPE, OWN_ID) "
                          "VALUES (%s, %s, %s, %s,%s, %s, %s, %s)")
        customer_data = (model, year, category, Daily_Rate,Weekly_Rate,Available,car_type,own_id)
        cursor.execute(add_customer_query, customer_data)
        conn.commit()
        return redirect('/')
    else:
    # redirect to success page
      return render_template('addcar.html')
    
# add owner
@app.route('/add_owner', methods=['GET','POST'])
def add_owner():
    # get form data
    if request.method=='POST':
        owner_name = request.form['owner_name']
        owner_type = request.form['owner_type']

        cursor = conn.cursor()
    
    # insert new customer data into database
        add_customer_query = ("INSERT INTO OWNER (OWNER_NAME, OWNER_TYPE) "
                          "VALUES (%s, %s)")
        customer_data = (owner_name,  owner_type)
        cursor.execute(add_customer_query, customer_data)
        conn.commit()
        return redirect('/')
    else:
    # redirect to success page
      return render_template('addowner.html')
    
# view car
@app.route('/view_car', methods=['GET', 'POST'])
def view_car():
    if request.method=='GET':
        select_records = ("SELECT * FROM CAR")
        cur.execute(select_records)
        records = cur.fetchall()
        return render_template('viewcar.html', records=records)
    return render_template('index.html')

# view car
@app.route('/view_customer', methods=['GET', 'POST'])
def view_customer():
    if request.method=='GET':
        select_records = ("SELECT * FROM CUSTOMER")
        cur.execute(select_records)
        records = cur.fetchall()
        return render_template('viewcustomer.html', records=records)
    return render_template('index.html')

# view report
@app.route('/view_report', methods=['GET', 'POST'])
def view_report():
    if request.method=='GET':
        select_records = ("SELECT CAR.CATEGORY, CAR.VEHICLE_ID, COUNT(CAR.VEHICLE_ID) AS UnitsOwned, SUM(CASE WHEN CAR.WEEKLY_RATE IS NULL THEN CAR.DAILY_RATE * RENTAL.NO_OF_DAYS + CAR.WEEKLY_RATE * RENTAL.NO_OF_WEEKS ELSE CAR.DAILY_RATE * ((RENTAL.NO_OF_DAYS DIV 7) * 7 + (RENTAL.NO_OF_DAYS MOD 7)) + CAR.WEEKLY_RATE * RENTAL.NO_OF_WEEKS END) AS TotalEarnings, SUM(CAR.DAILY_RATE * RENTAL.NO_OF_DAYS) / COUNT(DISTINCT CAR.VEHICLE_ID) AS DailyEarningsPerUnit, SUM(CASE WHEN CAR.WEEKLY_RATE IS NULL THEN 0 ELSE CAR.WEEKLY_RATE * RENTAL.NO_OF_WEEKS END) / COUNT(DISTINCT CAR.VEHICLE_ID) AS WeeklyEarningsPerUnit FROM RENTAL JOIN CAR ON RENTAL.V_ID = CAR.VEHICLE_ID GROUP BY CAR.CATEGORY, CAR.VEHICLE_ID;")
        cur.execute(select_records)
        records = cur.fetchall()
        return render_template('viewreport.html', records=records)
    return render_template('index.html')



# # update car
@app.route('/update_car', methods=['GET', 'POST'])
def update_car():
    if request.method == 'GET':
        # Get all the car records from the database
        select_records_query = "SELECT * FROM CAR"
        cur.execute(select_records_query)
        records = cur.fetchall()

        # Render the updatecar.html template with the car records
        return render_template('updatecar.html', records=records)
    else:
        # Get the updated car information from the form
        vehicle_id = request.form['vehicle_id']
        model = request.form['model']
        year = request.form['year']
        category = request.form['category']
        daily_rate = request.form['daily_rate']
        weekly_rate = request.form['weekly_rate']
        available = request.form['available']
        car_type = request.form['car_type']
        own_id = request.form['own_id']

        # Update the corresponding record in the database
        update_car_query = "UPDATE CAR SET MODEL=%s, YEAR=%s, CATEGORY=%s, DAILY_RATE=%s, WEEKLY_RATE=%s, AVAILABLE=%s, CAR_TYPE=%s, OWN_ID=%s WHERE VEHICLE_ID=%s"
        cur.execute(update_car_query, (model, year, category, daily_rate, weekly_rate, available, car_type, own_id, vehicle_id))
        conn.commit()
        
        return redirect('/')
    
# add rental    
@app.route('/add_rental', methods=['GET','POST'])
def add_rental():
    # get form data
    if request.method=='POST':
        status = request.form['status']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        amount_due = request.form['amount_due']
        rental_type = request.form['rental_type']
        no_of_days = request.form['no_of_days']
        no_of_weeks = request.form['no_of_weeks']
        customer_id= request.form['customer_id']
        vehicle_id= request.form['vehicle_id']
        # own_id = request.form['own_id']
        cursor = conn.cursor()
    
    # insert new customer data into database
        add_customer_query = ("INSERT INTO RENTAL (STATUS, START_DATE, END_DATE, AMOUNT_DUE, RENTAL_TYPE, NO_OF_DAYS, NO_OF_WEEKS,C_ID,V_ID) "
                          "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)")
        customer_data = (status, start_date, end_date, amount_due,rental_type,no_of_days,no_of_weeks,customer_id,vehicle_id)
        cursor.execute(add_customer_query, customer_data)
        conn.commit()
        return redirect('/')
    else:
    # redirect to success page
      return render_template('addrental.html')
    
# view rental
@app.route('/view_rental', methods=['GET', 'POST'])
def view_rental():
    if request.method=='GET':
        select_records = ("SELECT CAR.MODEL,CAR.CATEGORY, CAR.VEHICLE_ID, RENTAL.RENTAL_TYPE, RENTAL.START_DATE, RENTAL.END_DATE,CUSTOMER.C_TYPE, CUSTOMER.F_NAME, CUSTOMER.L_NAME, CUSTOMER.CUST_ID FROM RENTAL INNER JOIN CAR ON RENTAL.V_ID = CAR.VEHICLE_ID INNER JOIN CUSTOMER ON RENTAL.C_ID = CUSTOMER.CUST_ID;")
        cur.execute(select_records)
        records = cur.fetchall()
        return render_template('viewrental.html', records=records)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


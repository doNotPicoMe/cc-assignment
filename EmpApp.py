from flask import Flask, render_template, request,url_for,flash,redirect
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('HomePage.html')

@app.route("/home_page", methods=['GET', 'POST'])
def home_page():
    return render_template('HomePage.html')

@app.route("/search_employee", methods=['GET', 'POST'])
def search_employee():
    return render_template('SearchEmployee.html')


@app.route("/my_profile", methods=['GET', 'POST'])
def my_profile():
    return render_template('MyProfile.html')

@app.route("/employee_documentation", methods=['GET', 'POST'])
def employee_documentation():
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM employee")
    data = cursor.fetchall()
    return render_template('EmployeeDocumentation.html', data=data)

@app.route("/add_employee", methods=['GET', 'POST'])
def add_employee():
    return render_template('AddEmployee.html')

@app.route("/add_employee_function", methods=['POST'])
def add_employee_function():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    email = request.form['email']
    age = request.form['age']
    gender = request.form['gender']
    hire_date = request.form['hire_date']
    salary = request.form['salary']
    job = request.form['job']
    department = request.form['department']

    payroll_id= "OT"+emp_id
    late_hours= "0"
    overtime_hours= "0"
    emp_image_file = request.files['emp_image_file']

    insert_sql= "INSERT into employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
    insert_payroll_sql= "INSERT into payroll VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:
        cursor.execute(insert_sql,(emp_id,first_name,last_name,age,gender,location,pri_skill,email,department,job,salary,hire_date))
        db_conn.commit()
        cursor.execute(insert+payroll_sql,(payroll_id,late_hours,overtime_hours,emp_id))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)
        except Exception as e:
            return str(e)
    finally:
        cursor.close()

    # Not relevant to our design
    return render_template('EmployeeProfile.html', emp_id=emp_id,emp_name=emp_name,gender=gender,pri_skill=pri_skill, job=job,location=location, hire_date=hire_date,image_url="https://jeremy-employee.s3.amazonaws.com/emp-id-" + str(emp_id) + "_image_file")

@app.route("/delete_profile_function", methods=['GET', 'POST'])
def delete_profile_function():
    emp_id = request.form['emp_id']
    delete_employee_sql = "DELETE FROM employee where emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(delete_employee_sql,(emp_id))
    db_conn.commit()

    cursor.execute("SELECT * FROM employee")
    data = cursor.fetchall()

    if data == None:
        return render_template('EmployeeDocumentation.html')
    else:
        return render_template('EmployeeDocumentation.html', data=data)

@app.route("/search_employee_function", methods=['POST'])
def search_employee_function():
    emp_id = request.form['emp_id']

    search_sql= "SELECT *  FROM employee WHERE emp_id = (%s)"
    cursor = db_conn.cursor()
    emp_image_file_name_in_s3 = "https://jeremy-employee.s3.amazonaws.com/emp-id-" + str(emp_id) + "_image_file"
    try:
        cursor.execute(search_sql,(emp_id))
        records = cursor.fetchall()
        for row in records:
            first_name= row[1]
            last_name = row[2]
            age= row[3]
            gender= row[4]
            location= row[5]
            pri_skill= row[6]
            email= row[7]
            department= row[8]
            job= row[9]
            salary= row[10]
            hire_date= row[11]
            emp_name = "" + first_name + " " + last_name
    # iterate over the cursor

    finally:
        cursor.close()

    # Not relevant to our design
    return render_template('EmployeeProfile.html', emp_name=emp_name,gender=gender,pri_skill=pri_skill, job=job,location=location, hire_date=hire_date,image_url=emp_image_file_name_in_s3)

@app.route("/edit_profile_function", methods=['GET', 'POST'])
def edit_profile_function():
    emp_id = request.form['emp_id']

    search_sql= "SELECT *  FROM employee WHERE emp_id = (%s)"
    cursor = db_conn.cursor()
    try:
        cursor.execute(search_sql,(emp_id))
        records = cursor.fetchall()
        for row in records:
            emp_id= row[0]
            first_name= row[1]
            last_name = row[2]
            age= row[3]
            gender= row[4]
            location= row[5]
            pri_skill= row[6]
            email= row[7]
            department= row[8]
            job= row[9]
            salary= row[10]
            hire_date= row[11]
    # iterate over the cursor
    finally:
        cursor.close()
    return render_template('EditEmployeeProfile.html', emp_id=emp_id,first_name=first_name, last_name=last_name, age=age, gender=gender, location=location, pri_skill=pri_skill, email=email,department=department,job=job,salary=salary,hire_date=hire_date)

@app.route("/update_employee_function", methods=['GET', 'POST'])
def update_employee_function():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    email = request.form['email']
    age = request.form['age']
    gender = request.form['gender']
    hire_date = request.form['hire_date']
    salary = request.form['salary']
    job = request.form['job']
    department = request.form['department']
    search_sql= "SELECT *  FROM employee WHERE emp_id = (%s)"
    emp_image_file = request.files['emp_image_file']
    # update_sql= 'UPDATE employee SET first_name = "first_name", last_name = "last_name", age = "age", gender = "gender", location = "location", pri_skill= "pri_skill", email = "email", department = "department", job="job", salary ="salary", hire_date = "hire_date" WHERE emp_id = "emp_id"'
    update_sql= "UPDATE employee SET first_name=(%s), last_name=(%s), age=(%s), gender=(%s), location=(%s), pri_skill=(%s), email=(%s), department=(%s), job=(%s), salary=(%s), hire_date=(%s) WHERE emp_id=(%s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:
        cursor.execute(update_sql,(first_name,last_name,age,gender,location,pri_skill,email,department,job,salary,hire_date,emp_id))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)
        except Exception as e:
            return str(e)
    finally:
        cursor.close()

    # Not relevant to our design
    return render_template('EmployeeProfile.html', emp_id=emp_id,emp_name=emp_name,gender=gender,pri_skill=pri_skill, job=job,location=location, hire_date=hire_date,image_url="https://jeremy-employee.s3.amazonaws.com/emp-id-" + str(emp_id) + "_image_file")

@app.route("/payroll", methods=['GET', 'POST'])
def payroll():
    return render_template('Payroll.html')

@app.route("/payroll_deduction", methods=['GET', 'POST'])
def payroll_deduction():
    cursor = db_conn.cursor()
    cursor.execute("SELECT e.*,p.* FROM employee e, payroll p WHERE e.emp_id=p.emp_id")
    data = cursor.fetchall()

    if data == None:
        return render_template('PayrollDeduction.html')
    else:
        return render_template('PayrollDeduction.html', data=data)

@app.route("/add_payroll_deduction", methods=['GET', 'POST'])
def add_payroll_deduction():
    return render_template('AddPayrollDeduction.html')

@app.route("/add_payroll_deduction_function", methods=['GET', 'POST'])
def add_payroll_deduction_function():
    emp_id= request.form['emp_id']
    late_hours= request.form['overtime_hours']
    salary_sql="SELECT CAST(payroll as UNSIGNED INTEGER) FROM payroll WHERE emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(salary_sql,(emp_id))
    records = cursor.fetchall()
    for row in records:
        salary = row[0]

    salaryInt= int(salary)
    overtimeHoursInt= int(overtime_hours)
    # For every hour of OT, salary is increased by 100
    payroll = salaryInt - (overtimeHoursInt*10)
    payrollString = str(payroll)
    deduct_payroll_sql="INSERT into payroll VALUES (%s,%s,%s,%s,%s)"

    deduct_payroll_sql="UPDATE payroll VALUES late_hours=(%s),payroll=(%s) WHERE emp_id=(%s)"
    cursor.execute(deduct_payroll_sql,(late_hours,payroll,emp_id))
    db_conn.commit()

    cursor = db_conn.cursor()
    cursor.execute("SELECT e.*,p.* FROM employee e, payroll p WHERE e.emp_id=p.emp_id")
    data = cursor.fetchall()
    if data == None:
        return render_template('PayrollDeduction.html')
    else:
        return render_template('PayrollDeduction.html', data=data)


@app.route("/overtime", methods=['GET', 'POST'])
def overtime():
    cursor = db_conn.cursor()
    cursor.execute("SELECT e.*,p.* FROM employee e, payroll p WHERE e.emp_id=p.emp_id")
    data = cursor.fetchall()

    if data == None:
        return render_template('Overtime.html')
    else:
        return render_template('Overtime.html', data=data)

@app.route("/add_overtime", methods=['GET', 'POST'])
def add_overtime():
    return render_template('AddOvertime.html')

@app.route("/add_overtime_function",methods=['GET','POST'])
def add_overtime_function():
    emp_id= request.form['emp_id']
    salary_sql="SELECT CAST(payroll as UNSIGNED INTEGER) FROM payroll WHERE emp_id=(%s)"
    cursor = db_conn.cursor()
    cursor.execute(salary_sql,(emp_id))
    records = cursor.fetchall()

    for row in records:
        salary = row[0]

    overtime_hours= request.form['overtime_hours']
    salaryInt= int(salary)
    overtimeHoursInt= int(overtime_hours)

    # For every hour of OT, salary is increased by 100
    payroll = salaryInt + (overtimeHoursInt*100)
    payrollString = str(payroll)
    add_overtime_sql="UPDATE payroll VALUES overtime_hours=(%s),payroll=(%s) WHERE emp_id=(%s)"
    cursor.execute(add_overtime_sql,(overtime_hours, payrollString, emp_id))
    db_conn.commit()
    cursor.execute("SELECT e.*,p.* FROM employee e, payroll p WHERE e.emp_id=p.emp_id")
    data = cursor.fetchall()

    if data == None:
        return render_template('Overtime.html')
    else:
        return render_template('Overtime.html', data=data)

@app.route("/delete_overtime_function", methods=['GET', 'POST'])
def delete_overtime_function():
    emp_id=request.form['emp_id']
    late_hours="0"
    search_sql= "SELECT salary FROM employee WHERE emp_id = (%s)"
    cursor = db_conn.cursor()
    try:
        cursor.execute(search_sql,(emp_id))
        records = cursor.fetchall()
        for row in records:
            salary= row[0]
        # update_sql= 'UPDATE employee SET first_name = "first_name", last_name = "last_name", age = "age", gender = "gender", location = "location", pri_skill= "pri_skill", email = "email", department = "department", job="job", salary ="salary", hire_date = "hire_date" WHERE emp_id = "emp_id"'
        update_sql= "UPDATE payroll SET late_hours=(%s), salary=(%s) WHERE emp_id=(%s)"

        if emp_image_file.filename == "":
            return "Please select a file"
        try:
            cursor.execute(update_sql,(late_hours,salary,emp_id))
            db_conn.commit()
            cursor.execute("SELECT e.*,p.* FROM employee e, payroll p WHERE e.emp_id=p.emp_id")
            data = cursor.fetchall()
            if data == None:
                return render_template('Overtime.html')
            else:
                return render_template('Overtime.html', data=data)
        finally:
            cursor.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

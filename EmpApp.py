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
    return render_template('EmployeeDocumentation.html')

@app.route("/overtime", methods=['GET', 'POST'])
def overtime():
    return render_template('Overtime.html')

@app.route("/payroll", methods=['GET', 'POST'])
def payroll():
    return render_template('Payroll.html')

@app.route("/payroll_deduction", methods=['GET', 'POST'])
def payroll_deduction():
    return render_template('PayrollDeduction.html')

@app.route("/add_employee", methods=['GET', 'POST'])
def add_employee():
    return render_template('AddEmployee.html')

@app.route("/addemp", methods=['POST'])
def AddEmp():
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
    job_id= '1'
    dept_id= '1'
    emp_image_file = request.files['emp_image_file']
    resume_image_file = request.files['resume_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    if resume_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (emp_id, first_name, last_name,pri_skill, location,job_id,dept_id,gender,email,salary,hire_date,age))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        resume_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            s3.Bucket(custombucket).put_object(Key=resume_image_file_name_in_s3, Body=resume_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3,
                resume_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    # Not relevant to our design
    print("all modification done...")
    return render_template('EmployeeProfile.html', name=emp_name,gender=gender,pri_skill=pri_skill, location=location)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

# @app.route("/addemp", methods=['GET'])
# def AddEmp():
# select_employee = """SELECT * FROM employee"""
# cursor = conn.cursor()
# cursor.execute(select_employee)
# result = cursor.fetchall()
#
# for row in result:
#     emp_id     = %row[0]
#     first_name = %row[1]
#     last_name  = %row[2]
#     pri_skill  = %row[3]
#     location   = %row[4]
#     gender     = %row[5]
#
#     emp_name = "" + first_name + " " + last_name
#     break
#
# left is html, right is python script
#     return render_template('employeeDocumentation.html', emp_id=emp_id, emp_name=emp_name, pri_skill=pri_skill,location=location)

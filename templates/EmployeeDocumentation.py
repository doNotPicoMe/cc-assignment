# Python CODE
import mysql.connector
import webbrowser

conn = mysql.connector.connect(user='admin', password='12345678',
                              host='cc-assignment.czz0hfqvljiq.us-east-1.rds.amazonaws.com',database='employee')
if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")

select_employee = """SELECT * FROM employee"""
cursor = conn.cursor()
cursor.execute(select_employee)
result = cursor.fetchall()

p = []

tbl = "<thead>
    <tr>
      <th scope="col">Work ID</th>
      <th scope="col">Name</th>
      <th scope="col">Gender</th>
      <th scope="col">Age</th>
      <th scope="col">Department</th>
      <th scope="col">Salary (RM)</th>
      <th scope="col">Email</th>
      <th scope="col">Hire Date</th>
      <th scope="col">Resume</th>
      <th scope="col">Edit Profile</th>
    </tr>
  </thead>"
p.append(tbl)

for row in result:
    emp_id = "<td data-title="row">%s</td>"%row[1]
    p.append(emp_id)

    emp_name= "<td data-title="Name">%s</td>"emp_name = "" + %row[1] + " " + %row[2]
    p.append(emp_name)

    gender = "<td data-title="Gender">%s</td>"%row[8]
    p.append(gender)

    age = "<td data-title="Age">%s</td>"%row[2]
    p.append(age)

    department = "<td data-title="department">%s</td>"%row[7]
    p.append(department)

    salary = "<td data-title="salary">%s</td>"%row[10]
    p.append(salary)

    email = "<td data-title="email">%s</td>"%row[9]
    p.append(email)

    hire_date = "<td data-title="hire_date">%s</td>"%row[11]
    p.append(hire_date)


# HTML FILE

<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>Employee-Documentation</title>
  <link rel="icon" href="../static/tab_logo.png">
  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.css'>
  <link rel='stylesheet' href='https://unpkg.com/ionicons@4.5.10-0/dist/css/ionicons.min.css'>
  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/material-design-icons/3.0.2/iconfont/material-icons.min.css'>
  <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='NavBarStyle.css') }}">
  <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='TableStyle.css') }}">
</head>

<header class="header">
  <nav class="navbar">
    <span class="open-menu">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="16">
        <g fill="#252a32" fill-rule="evenodd">
          <path d="M0 0h24v2H0zM0 7h24v2H0zM0 14h24v2H0z" />
        </g>
      </svg>
    </span>
    <h1><a href="./HomePage.html" class="brand">FCUC Enterprise Solutions</a></h1>
    <div class="menu-wrapper">
      <ul class="menu">
        <li class="menu-block">
          <span class="close-menu">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20">
              <path fill="#252a32" fill-rule="evenodd" d="M17.778.808l1.414 1.414L11.414 10l7.778 7.778-1.414 1.414L10 11.414l-7.778 7.778-1.414-1.414L8.586 10 .808 2.222 2.222.808 10 8.586 17.778.808z" />
            </svg>
          </span>
        </li>
        <li class="menu-item"><a href="./MyProfile.html" class="menu-link">My Profile</a></li>
        <li class="menu-item"><a href="./HomePage.html" class="menu-link">Home Page</a></li>
        <li class="menu-item has-collapsible">
          <a href="#"><span></span>Employee</a>
          <ul class="menu-child">
            <li class="menu-child-item"><a href="./AddEmployee.html">Add</a></li>
            <li class="menu-child-item"><a href="./SearchEmployee.html">Search</a></li>
            <li class="menu-child-item"><a href="./EmployeeDocumentation.html">Documentation</a></li>
          </ul>
        </li>
        <li class="menu-item has-collapsible">
          <a href="#"><span></span>Payroll</a>
          <ul class="menu-child">
            <li class="menu-child-item"><a href="./Overtime.html">Overtime Payment</a></li>
						<li class="menu-child-item"><a href="./PayrollDeduction.html">Payroll Deduction</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>
</header>
<body>
  <div class="container">
    <table class="responsive-table">
      <caption>Employee Documentation</caption>
      <thead>
        <tr>
          <th scope="col">Work ID</th>
          <th scope="col">Name</th>
          <th scope="col">Gender</th>
          <th scope="col">Age</th>
          <th scope="col">Department</th>
          <th scope="col">Salary (RM)</th>
          <th scope="col">Email</th>
          <th scope="col">Hire Date</th>
          <th scope="col">Resume</th>
          <th scope="col">Edit Profile</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">B1499</th>
          <td data-title="Name">JEREMY PUN KHENG MING</td>
          <td data-title="Gender">Male</td>
          <td data-title="Age">21</td>
          <td data-title="Department">Information Technology</td>
          <td data-title="Salary" data-type="currency">$1,657,870,986</td>
          <td data-title="Email">b1499@student.firstcity.edu.my</td>
          <td data-title="Hire Date">OCT 2020</td>
          <td data-title="Resume"><button id="resumeButton" type="button">view</button></td>
          <td data-title="Edit Profile"><button id="editButton" type="button">edit</button></td>
        </tr>
        <tr>
          <th scope="row">B1499</th>
          <td data-title="Name">{{emp_name}}</td>
          <td data-title="Gender">{{gender}}</td>
          <td data-title="Age">21</td>
          <td data-title="Department">Information Technology</td>
          <td data-title="Salary" data-type="currency">$1,657,870,986</td>
          <td data-title="Email">b1499@student.firstcity.edu.my</td>
          <td data-title="Hire Date">OCT 2020</td>
          <td data-title="Resume"><button id="resumeButton" type="button">view</button></td>
          <td data-title="Edit Profile"><button id="editButton" type="button">edit</button></td>
        </tr>
        <tr>
          %s
          <td data-title="Resume"><button id="resumeButton" type="button">view</button></td>
          <td data-title="Edit Profile"><button id="editButton" type="button">edit</button></td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="7">Data is current as of March 31, 2021.</td>
        </tr>
      </tfoot>
    </table>
  </div>
  <script src="https://unpkg.com/sweetalert2@7.8.2/dist/sweetalert2.all.js"></script>
  <script>
  //get a reference to the element
  var resume = document.getElementById('resumeButton');
  var edit = document.getElementById('editButton');

  //add event listener
  resume.addEventListener('click', function(event) {
    swal({
      title: "Are you sure?",
      text: "You will not be able to recover this imaginary file!",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: '#DD6B55',
      confirmButtonText: 'Yes, I am sure!',
      cancelButtonText: "No, cancel it!",
      closeOnConfirm: false,
      closeOnCancel: false
    },
    .then(() => {
      dispatch(redirect('/'));
    });
  });
  edit.addEventListener('click', function(event) {
    swal({
      title: 'Employee was successfully added!',
      type: 'success',
    }).then(() => {
      if (result.value) {
        // handle Confirm button click
      } else {
        // result.dismiss can be 'cancel', 'overlay', 'esc' or 'timer'
      }
    });
  });
  </script>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
  <script  src="{{ url_for("static",filename='NavBarScript.js') }}"></script>
  <script  src="../static/NavBarScript.js"></script>
</body>
</html>
'''%(p)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

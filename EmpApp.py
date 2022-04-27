<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="../static/tab_logo.png">
  <title>Payroll-Add Overtime</title>
  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.css'>
  <link rel='stylesheet' href='https://unpkg.com/ionicons@4.5.10-0/dist/css/ionicons.min.css'>
  <!-- NAVBAR > icon -->
  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/material-design-icons/3.0.2/iconfont/material-icons.min.css'>
  <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='NavBarStyle.css') }}">
  <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='FormStyle.css') }}">
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
    <h1><a href="{{ url_for('home_page') }}" class="brand">FCUC Enterprise Solutions</a></h1>
		<div class="menu-wrapper">
			<ul class="menu">
				<li class="menu-block">
					<span class="close-menu">
						<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20">
							<path fill="#252a32" fill-rule="evenodd" d="M17.778.808l1.414 1.414L11.414 10l7.778 7.778-1.414 1.414L10 11.414l-7.778 7.778-1.414-1.414L8.586 10 .808 2.222 2.222.808 10 8.586 17.778.808z" />
						</svg>
					</span>
				</li>
        <li class="menu-item"><a href="{{ url_for('my_profile') }}" class="menu-link">My Profile</a></li>
        <li class="menu-item"><a href="{{ url_for('home_page') }}" class="menu-link">Home Page</a></li>
        <li class="menu-item has-collapsible">
          <a><span></span>Employee</a>
          <ul class="menu-child">
            <li class="menu-child-item"><a href="{{ url_for('add_employee') }}">Add</a></li>
            <li class="menu-child-item"><a href="{{ url_for('search_employee') }}">Search</a></li>
            <li class="menu-child-item"><a href="{{ url_for('employee_documentation') }}">Documentation</a></li>
          </ul>
        </li>
        <li class="menu-item has-collapsible">
					<a><span></span>Payroll</a>
					<ul class="menu-child">
						<li class="menu-child-item"><a href="{{ url_for('overtime') }}">Overtime Payment</a></li>
						<li class="menu-child-item"><a href="{{ url_for('payroll_deduction') }}">Payroll Deduction</a></li>
					</ul>
				</li>
			</ul>
		</div>
	</nav>
</header>
<body>
  <div class="login-page">
    <div class="animated slideInUp form">
    <center><img style="height:110px; width:auto;" src="../static/fcuc_logo.png" alt="fcuc_logo"></center></br></br>
      <form class="login-form" action="/add_overtime_function" autocomplete="on" method = "POST" enctype="multipart/form-data">
        <input type="text" name="emp_id" placeholder="Employee ID"/>
        <input type="text" name="overtime_hours" placeholder="Number of overtime hours"/>
        <button type="submit" id="overtimeButton">Add Overtime Pay</button>
      </form>
    </form>
    </div>
  </div>
  <script src="https://unpkg.com/sweetalert2@7.8.2/dist/sweetalert2.all.js"></script>
  <script>
  //get a reference to the element
  var overtime = document.getElementById('overtimeButton');
  //add event listener
  overtime.addEventListener('click', function(event) {
    swal({
      title: 'Overtime was successfully added!',
      type: 'success',
    })
    .then(() => {
        // dispatch(redirect('/'));
    });
  });
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script  src="{{ url_for("static",filename='AddEmpScript.js') }}"></script>
<script  src="{{ url_for("static",filename='NavBarScript.js') }}"></script>
</body>
</html>

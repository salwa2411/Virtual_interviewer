var user = document.querySelector('#user');
user.addEventListener('keyup', function(){
	var u_times = document.querySelector('.u_times');
	var u_check = document.querySelector('.u_check');
	if (user.value.length == 0 || user.value.length < 6){
		user.style.border = '1px solid red';
		u_times.style.display = 'block';
		u_check.style.display = 'none';
		return false;
	}
	else{
		user.style.border = '1px solid green';
		u_times.style.display = "none";
		u_check.style.display = "block";
	}
})

var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
// var reg = String.raw`\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2-3,}\b`
// let strongEmail = new RegExp("[a-z0-9]+@[a-z]+\.[a-z]{2,4}","g");	
let strongEmail = new RegExp("^([a-zA-Z0-9_.-]+)@([a-zA-Z]+)([\.])(com)$","g");

var pass = document.querySelector('#pass');
var pass1 = document.querySelector('#pass1');

pass.addEventListener('keyup', function(){
	var p_times = document.querySelector('.p_times');
	var p_check = document.querySelector('.p_check');
	// var p_times1 = document.querySelector('.p_times1');
	// var p_check1 = document.querySelector('.p_check1');
	
	if (strongRegex.test(pass.value)){
		pass.style.border = '1px solid green';
		p_times.style.display = "none";
		p_check.style.display = "block";
		document.getElementById('password-strength-status').style.color = "green";
		document.getElementById('password-strength-status').innerHTML = "Strong Password";
		return false;
	}
	else if (pass.value.length > 0 && pass.value.length < 8) {
		pass.style.border = '1px solid red';
		p_times.style.display = 'block';
		p_check.style.display = 'none';
		document.getElementById('password-strength-status').style.color = "red";
		document.getElementById('password-strength-status').innerHTML = "Weak Password";
		return false;
	}
	else if (pass.value.length == 0){
		document.getElementById('password-strength-status').style.color = "red";
		document.getElementById('password-strength-status').innerHTML = "*Please fill the required fields!";
		return false;
	}


	
})



pass1.addEventListener('keyup', function(){
	var p_times1 = document.querySelector('.p_times1');
	var p_check1 = document.querySelector('.p_check1');
	if (pass1.value.length>0 && pass.value == pass1.value){
		if (strongRegex.test(pass1.value)){
			pass1.style.border = '1px solid green';
			p_times1.style.display = "none";
			p_check1.style.display = "block";
			document.getElementById('password-strength-status').style.color = "green";
			document.getElementById('password-strength-status').innerHTML = "password matched";
		}
		else{
			pass1.style.border = '1px solid red';
			p_times1.style.display = 'block';
			p_check1.style.display = 'none';
			document.getElementById('password-strength-status').style.color = "red";
			document.getElementById('password-strength-status').innerHTML = "Weak Password";

		}	
		

	}
	else if (pass.value != pass1.value) {
		pass1.style.border = '1px solid red';
		p_times1.style.display = 'block';
		p_check1.style.display = 'none';
		document.getElementById('password-strength-status').style.color = "red";
		document.getElementById('password-strength-status').innerHTML = "mismatch password";
	}

})

// pass1.addEventListener('keyup', function(){
// 	var p_times = document.querySelector('.p_times');
// 	var p_check = document.querySelector('.p_check');
// 	// var p_times1 = document.querySelector('.p_times1');
// 	// var p_check1 = document.querySelector('.p_check1');
	
// 	if (strongRegex.test(pass1.value)){
// 		pass1.style.border = '1px solid green';
// 		p_times.style.display = "none";
// 		p_check.style.display = "block";
// 		document.getElementById('password-strength-status').style.color = "green";
// 		document.getElementById('password-strength-status').innerHTML = "Strong Password";
// 		return false;
// 	}
// 	else if (pass1.value.length > 0 && pass1.value.length < 8) {
// 		pass1.style.border = '1px solid red';
// 		p_times.style.display = 'block';
// 		p_check.style.display = 'none';
// 		document.getElementById('password-strength-status').style.color = "red";
// 		document.getElementById('password-strength-status').innerHTML = "Weak Password";
// 		return false;
// 	}
// 	else if (pass1.value.length == 0){
// 		document.getElementById('password-strength-status').style.color = "red";
// 		document.getElementById('password-strength-status').innerHTML = "*Please fill the required fields!";
// 		return false;
// 	}


	
// })

var email = document.querySelector('#mail');
email.addEventListener('keyup', function(){
	var e_times = document.querySelector('.e_times');
	var e_check = document.querySelector('.e_check');
	if (strongEmail.test(email.value)){
		
		email.style.border = '1px solid green';
		e_times.style.display = "none";
		e_check.style.display = "block";
		document.getElementById('password-strength-status').style.color = "green";
		document.getElementById('password-strength-status').innerHTML = "Valid Email";
		console.log(strongRegex.test(pass.value))
		return false;

	}
	else {
		email.style.border = '1px solid red';
		e_times.style.display = 'block';
		e_check.style.display = 'none';
		document.getElementById('password-strength-status').style.color = "red";
		document.getElementById('password-strength-status').innerHTML = "Please Enter Correct Email";
		return false;
		}
		
})

function validate(){
	if (user.value == 0 || user.value.length < 6){
		document.getElementById('password-strength-status').style.color = "red";
		document.getElementById('error').innerHTML = "Please fill the required fields!";
		return false;
	}
}
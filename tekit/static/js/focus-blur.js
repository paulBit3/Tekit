//Checking username

function checkUsername() {                        
	var username = el.value;
	if (username.length < 10) {
		elMsg.className = 'warning';
		elMsg.textContent = 'Too short!';
	} else {
		elMsg.textContent = '';
	}
}

function tipUsername() {
	elMsg.className = 'tip';
  	elMsg.innerHTML = 'Username must be at least 10 characters'; 
}

var el = document.getElementById('username');     // Username input
var elMsg = document.getElementById('feedback');

//Check if el not null
if(el) {
	el.addEventListener('focus', tipUsername, false);
	el.addEventListener('blur', checkUsername, false); 
}


//creating focus on textinuput when necessary on a page Laod

//Login focus
function setup() {
	var textInput;
	textInput = document.getElementById('username').focus();
	// textInput.focus();
}

window.addEventListener('load', setup, false);

//Register focus
function resetup() {
	var text2Input;
	text2Input = document.getElementById('first_name').focus();
	// textInput.focus();
}

window.addEventListener('load', resetup, false);
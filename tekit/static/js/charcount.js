
//Count text area character for comment
var el;

function charCount(e) {
	var textEntered, charDisplay, counter, max_len;
  	textEntered = document.getElementById("content").value;
  	charDisplay = document.getElementById("charactersLeft");
  	max_len = 160;
    len = (max_len - (textEntered.length));

    // len = max_len - len;
  	// 

    if (len < 0) {
      charDisplay.textContent = len;
      document.getElementById("char_count").innerHTML = '<span style="color: red;">You have exceeded the limit of '+ max_len +' characters</span>';
    } else {
      charDisplay.textContent = '';
      document.getElementById("char_count").innerHTML = len + ' character' + (len == 1 ? '' : 's')  + ' remaining.';
    }

    // $('#char_count').text(len > 0 ? (len + ' character' + (len == 1 ? '' : 's')  + ' remaining.') : '');
    // console.log(len)
   

}


el = document.getElementById("content");
el.addEventListener('keyup', charCount, false);




//Count text area character for comment reply
var el;

function charreplyCount(e) {
	var textEntered, charDisplay, counter, max_len;
  	textEntered = document.getElementById("contents").value;
  	charDisplay = document.getElementById("charactersReplyLeft");
    max_len = 160;
  	len = (max_len - (textEntered.length));

    if (len < 0) {
      charDisplay.textContent = len;
      document.getElementById("repchar_count").innerHTML = '<span style="color: red;">You have exceeded the limit of '+ max_len +' characters</span>';
    }else {
      charDisplay.textContent = '';
      document.getElementById("repchar_count").innerHTML = len + ' character' + (len == 1 ? '' : 's')  + ' remaining.';
    }

  	// charDisplay.textContent = len;
    // var len = $(this).val().trim().length;
    // $('#repchar_count').text(len > 0 ? (len + ' character' + (len == 1 ? '' : 's')  + ' remaining.') : '');

}

el = document.getElementById("contents");
el.addEventListener('keyup', charreplyCount, false);



function countChar1(val) {
  var len = val.value.length;
  var color;
  $('charactersLeft').text(0 + len);

  color = len < 100 ? 'red' : 'green';
  $('charactersLeft').css({
    'color': color
  });
};
/* 1. Proloder */

(function ($)
  { "use strict"
  
/* 1. Proloder */
    $(window).on('load', function () {
      $('#preloader-active').delay(450).fadeOut('slow');
      $('body').delay(450).css({
        'overflow': 'visible'
      });
    });

})(jQuery);


/* Time out for messages */

setTimeout(function() {
  $('.message').fadeOut('slow');
}, 2000);


// loading image or picture

    $('#inputfile').on('change',function(){
        //get the file name
        var fileName = $(this).val();
        //replace the "Choose a file" label
        $(this).next('.custom-file-label').html(fileName);
    })

 // user send friend request
    $('.js-sendRequest').click(function(e) {
        e.preventDefault();

        var thisId = $(this).attr('id'),
            idPair = thisId.replace('send_request_', '').split('_'),
            fromId = idPair[0].replace('from', ''),
            toId = idPair[1].replace('to', '');

        $.ajax({
            url: '/user/request/',
            type: 'GET',
            dataType: 'json',
            data: {
                request_type: 'send',
                from_user_id: fromId,
                to_user_id: toId,
                message: 'Hi, sent you an invitation'
            },
            success: function (resp) {
                if (resp.result === 'Sent successfully') {
                    alert('Sent request successfully');
                    $('#'+thisId).hide();
                }
            }
        });
    });

    // user accept friend request
    $('.js-acceptRequest').click(function(e) {
        e.preventDefault();

        var thisId = $(this).attr('id'),
            idPair = thisId.replace('accept_request_', '').split('_'),
            fromId = idPair[0].replace('from', ''),
            toId = idPair[1].replace('to', '');

        $.ajax({
            url: '/user/request/',
            type: 'GET',
            dataType: 'json',
            data: {
                request_type: 'accept',
                from_user_id: fromId,
                to_user_id: toId
            },
            success: function(json){
                alert(json['result']);
                $("#"+thisId).parent().hide();
            }
        });
    });


// display comment form
function showForm() {
    var x = document.getElementById("id-input");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}



//managing comment and reply form


 // Reply to comment
// $(".reply-btn").click(function(event){
//     event.preventDefault();
//     $(this).parent().next(".comment-reply").fadeToggle();
// })

// $(document).ready(function () {
//   $(".reply-btn").click(function() {
//     $(".comment-reply").fadeToggle();
//   });
// });



// Back to top page
var btn = $('.back-to-top');

$(window).scroll(function() {
  if ($(window).scrollTop() > 300) {
    btn.addClass('show');
  } else {
    btn.removeClass('show');
  }
});

btn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});




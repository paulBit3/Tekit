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
    var x = document.getElementById("myDiv");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}


// validate comment and reply form
function validateForm() {
    var form = document.forms['cmntForm']['content'].value;
    if (form == '') {
        alert('Required: Type a comment before submit!');
        return false;
    }
}



//managing comment and reply form

var formTemplate = document.querySelector('#form-template form');
var idInput = document.getElementById('id-input');

function toggleReply(e) {
  if (!formTemplate) return;

  e.target.parentNode.insertBefore(formTemplate, e.target);
  idInput.value = e.target.getAttribute('data-id');
};

Array.from(document.querySelectorAll('button.reply'))
  .forEach(btn => btn.onclick = toggleReply)

Array.from(document.querySelectorAll('button.cmt-btn'))
  .forEach(btn => btn.onclick = toggleReply)

 // Reply to comment
 // $('.reply-btn').click(function() {
 //    $(this).parent().reply().next('.comments-replied').fadeToggle()
 // });


(function($) {
  
  "use strict";  

  $(window).on('load', function() {

    /* 
   MixitUp
   ========================================================================== */
  $('#portfolio').mixItUp();

  /* 
   One Page Navigation & wow js
   ========================================================================== */
    var OnePNav = $('.onepage-nev');
    var top_offset = OnePNav.height() - -0;
    OnePNav.onePageNav({
      currentClass: 'active',
      scrollOffset: top_offset,
    });
  
  /*Page Loader active
    ========================================================*/
    $('#preloader').fadeOut();

  // Sticky Nav
    $(window).on('scroll', function() {
        if ($(window).scrollTop() > 200) {
            $('.scrolling-navbar').addClass('top-nav-collapse');
        } else {
            $('.scrolling-navbar').removeClass('top-nav-collapse');
        }
    });

    /* slicknav mobile menu active  */
    $('.mobile-menu').slicknav({
        prependTo: '.navbar-header',
        parentTag: 'liner',
        allowParentLinks: true,
        duplicate: true,
        label: '',
        closedSymbol: '<i class="icon-arrow-right"></i>',
        openedSymbol: '<i class="icon-arrow-down"></i>',
      });

      /* WOW Scroll Spy
    ========================================================*/
     var wow = new WOW({
      //disabled for mobile
        mobile: false
    });

    wow.init();

    /* Nivo Lightbox 
    ========================================================*/
    $('.lightbox').nivoLightbox({
        effect: 'fadeScale',
        keyboardNav: true,
      });

    /* Counter
    ========================================================*/
    $('.counterUp').counterUp({
     delay: 10,
     time: 1000
    });


    /* Back Top Link active
    ========================================================*/
      var offset = 200;
      var duration = 500;
      $(window).scroll(function() {
        if ($(this).scrollTop() > offset) {
          $('.back-to-top').fadeIn(400);
        } else {
          $('.back-to-top').fadeOut(400);
        }
      });

      $('.back-to-top').on('click',function(event) {
        event.preventDefault();
        $('html, body').animate({
          scrollTop: 0
        }, 600);
        return false;
      });



  });      

}(jQuery));
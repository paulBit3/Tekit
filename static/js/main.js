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

 



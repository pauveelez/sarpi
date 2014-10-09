$(document).ready(function(){
    var $button = $('#btn-feed');
    var $counter = $('.btn--feedText');


    var time = 0;
    var timer;

    var counter = function(){
        $counter.fadeOut(500).fadeIn(500);
        $counter.text(++time);
    };
    var interval = function(){
        timer = setInterval(counter,1000);
    };
    var clean = function(){
        clearInterval(timer);
        if(time > 0){
            var msg;
            if (time > 1)
                msg = "segundos";
            else
                msg = "segundo";

            swal({
                title: "",
                text: "¿Servir una porción de: "+time+" "+msg+"?",
                type: "info",
                cancelButtonText: "Aun no",
                showCancelButton: true,
                confirmButtonColor: "#4AA2E9",
                confirmButtonText: "Claro!" },
                function(){
                    $counter.text("Feed me!");
                    var data = {'seconds':time};
                    var xhr = $.post('/ajax_feed',data);
                    xhr.done(function(){
                        time = 0;
                        setTimeout(function(){
                            swal("Genial", "Estamos sirviendo la comida!", "success");
                            setTimeout(function(){
                                $('.confirm').trigger('click');
                            },2000);
                        },200);

                    });
            });
        }
    };
    if( navigator.userAgent.match(/Android/i) ||
        navigator.userAgent.match(/webOS/i) ||
        navigator.userAgent.match(/iPhone/i) ||
        navigator.userAgent.match(/iPad/i) ||
        navigator.userAgent.match(/iPod/i) ||
        navigator.userAgent.match(/BlackBerry/i)||
        navigator.userAgent.match(/Windows Phone/i)
     ){
        $button.on('touchstart',interval);
        $button.on('touchend',clean);
      }
     else {
        $button.on('mousedown',interval);
        $button.on('mouseup',clean);
      }

      $('body').on('click','.cancel',function(){
            $counter.text("Feed me!");
            time = 0;
      });
});
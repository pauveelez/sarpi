$(function(){
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
        //reemplazar por una confirmación o un ajax lindo
        clearInterval(timer);
        if(time > 0){
            var msg;
            if (time > 1)
                msg = "segundos";
            else
                msg = "segundo";
            var p = confirm("Crear una porcion de: "+time+" "+msg);
            if(p){
                time = 0;
                $counter.text("Feed me!");
                var data = {'seconds':time};
                var xhr = $.post('/ajax_feed',data);
                xhr.done = function(){
                    alert('ajax a funcionado bien');
                    // debugger;
                };
                //mandar ajax y resetear el contador
            }else{
                // dejar el contador como está
            }
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


});
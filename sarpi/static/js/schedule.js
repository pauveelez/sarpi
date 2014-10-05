$(function(){
    // $('#Schedule').datetimepicker({
    //     step:5,
    //     inline:true
    // });
    $(".responsive-calendar").responsiveCalendar({
      // time: '2013-05',
      events: events,
      translateMonths: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],

    });
});
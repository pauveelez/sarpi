$(function(){
    var events = {};
    for(i = 0, emp; i < data.length; i++){
        var emp = data[i];
        if(events[ emp.date_start ]){
            events[ emp.date_start ].push(emp);
        }else{
            events[ emp.date_start ] = [emp];
        }
    }

    // console.log(events)
    var months = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre"
    ];
    var $details = $('#details');
    var $detailsTitle = $('#details-title');
    var $detailsDescription = $('#details-description');
    var $detailsList = $('#details-list');
    var $detailsEdit = $('#details-edit');
    var $Schedule = $("#Schedule");
    $Schedule.responsiveCalendar({
      // time: '2013-05',
      events: events,
      translateMonths: months,
      onActiveDayClick : function(event){

        $detailsList.empty();
        $details.addClass('is-active');
        var self = this;
        var $self = $(this);

        if(self.dataset.day <= 9){
            self.dataset.day = "0"+self.dataset.day;
        }

        var scheduleString = self.dataset.year +"-"+ self.dataset.month +"-"+ self.dataset.day;
        var schedule = events[scheduleString];
        var scheduleFirst = schedule[0];

        $detailsTitle.text(scheduleFirst.date_start);
        $detailsDescription.text(scheduleFirst.description);
        $detailsEdit.text("Eliminar");


        var dayWithZero = self.dataset.day;
        if (dayWithZero.charAt(0) == '0'){
          self.dataset.day = dayWithZero.substr(1);
        }

        for(i = 0, total = schedule.length; i <= total; i++){
            $detailsList.append('<li>'+schedule[i].time_start+'</li>');
        }
      },
      onMonthChange :function (){
        $details.removeClass('is-active');
      },
      onDayClick : function (event){
        $detailsList.empty();
        $details.addClass('is-active');
        var self = this;
        var $self = $(this);

        if(self.dataset.day <= 9){
            self.dataset.day = "0"+self.dataset.day;
        }

        var scheduleString = self.dataset.year +"-"+ self.dataset.month +"-"+ self.dataset.day;

        $detailsTitle.text(scheduleString);
        $detailsDescription.text('No Hay Horario Programado');
        $detailsEdit.text("Crear");
        $detailsEdit.attr("href","/schedule/"+scheduleString);

        var dayWithZero = self.dataset.day;
        if (dayWithZero.charAt(0) == '0'){
          self.dataset.day = dayWithZero.substr(1);
        }
      },
    });

    $('.Schedule-year_').on('click',function(){
        var $self = $(this);
        var id = $self.attr('id');
        if(id == "year-next"){
            for(i=0;i<=11;i++){
                $Schedule.responsiveCalendar('next');
            }
        }else{
            for(i=0;i<=11;i++){
                $Schedule.responsiveCalendar('prev');
            }
        }
    });
});
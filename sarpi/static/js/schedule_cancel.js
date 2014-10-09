$(function(){
    var $detailsEdit = $('#details-edit');
    $detailsEdit.click(function() {
        var date_cancel = $('#details-title').text();
        if($detailsEdit.text() == 'Cancelar'){
            $detailsEdit.attr("href","/schedule");
            var p = confirm("Desea cancelar los horarios del dia \n \n"+date_cancel);
            if(p){
                var data = {'date':date_cancel};
                var xhr = $.post('/schedule_ajax',data);
                xhr.done(function(){
                   // Todo OK se elimino el horario
                });
                //mandar ajax y resetear el contador
            }else{
                // dejar el contador como está
            }
        }
    });
});
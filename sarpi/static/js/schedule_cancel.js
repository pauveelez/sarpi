$(function(){
    var $detailsEdit = $('#details-edit');
    $detailsEdit.click(function() {
        var date_cancel = $('#details-title').text();
        if($detailsEdit.text() == 'Eliminar'){
            $detailsEdit.attr("href","#");
            swal({
                title: "",
                text: "¿Deseas cancelar los horarios del dia: "+date_cancel+"?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: '#4AA2E9',
                confirmButtonText: 'Claro!',
                closeOnConfirm: false
            },
            function(){
                var data = {'date':date_cancel};
                var xhr = $.post('/schedule_ajax',data);
                xhr.done(function(){
                    setTimeout(function(){
                        swal("Genial", "Se canceló el horario deseado", "success");
                        setTimeout(function(){
                            $('.confirm').trigger('click');
                        },2000);
                    },200);
                    location.reload();
                });
            });
        }
    });
});
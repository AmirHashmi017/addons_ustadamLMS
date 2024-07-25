const popupButton = document.getElementById('Coach');
const popupBlock = document.getElementById('modal_view');


$(document).ready(function(){
    $("#modal_view").modal("hide");
    $("#btnHandler").click(function(){
        $("#modal_view").modal("hide");
      });
    $("#Coach").click(function(){
      $("#modal_view").modal("show");
    });
});

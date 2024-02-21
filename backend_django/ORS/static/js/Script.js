//function selectAll(source) {
//    checkboxes = document.getElementsByName('ids');
//    for (var i = 0, n = checkboxes.length; i < n; i++) {
//        checkboxes[i].checked = source.checked;
//    }
//}
//
//function selectone(so) {
//    checkboxes = document.getElementById('mainbox');
//    unbox = document.getElementsByName('ids');
//    var box = false;
//    for (var i = 0, n = unbox.length; i < n; i++) {
//        if (unbox[i].checked == true) {
//            box = true;
//        } else {
//            box = false;
//            break;
//        }
//    }
//    checkboxes.checked = box;
//}

$(document).ready(function (){
    txt = ""
    $('#select_all').on("click",function(){

        if(this.checked){
            $('.checkbox').each(function(){
                this.checked = true;
                txt = $(this).val();
            });
        }else{
            $('.checkbox').each(function(){
                this.checked = false;
                txt = $(this).val();
            });
        }
    });
    $('.checkbox').on('click', function(){
        if ($('.checkbox:checked').length == $('.checkbox').length){
            $('#select_all').prop('checked', true);
            txt = $(this).val();
        }else{
            $('#select_all').prop('checked', false)
            txt = $(this).val();
        }
    });
    $('#ids').val(txt)
})


$(function (){
    setTimeout(function(){
        $('#timeout').fadeOut(1000);
    }, 3000)
})
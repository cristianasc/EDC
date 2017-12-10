function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$("#comment").click(function () {
    text_to_comment = $("#text_to_comment").val();
    console.log(text_to_comment);

    fd = new FormData();
    fd.append("comment", text_to_comment);


    $.ajax({
        url: '/comments/',
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
    });

});

function del(id) {
    fd = new FormData();
    fd.append('uid', id);

    $.ajax({
        url: '/del_new/',
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
    });
}
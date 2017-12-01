function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function delnew(new_id) {

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    fd = new FormData();
    fd.append('uid', new_id);

    $.ajax({
        url: '/del_new/',
        data: fd,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data) {
            $('div[rel="new'+new_id.replace("c=", "")+'"]').hide();
        }
    });
}
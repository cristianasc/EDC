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
    var text_to_comment = $("#text_to_comment").val();
    var music_id = window.location.href.split("=");
    music_id = music_id[music_id.length-1];

    fd = new FormData();
    fd.append("comment", text_to_comment);
    fd.append("music_id", music_id);

    $.ajax({
        url: '/comments/',
        data: fd,
        async: false,
        processData: false,
        contentType: false,
        type: 'POST'
    }).done(function() {
        window.location.reload();
    });
    return false;
});

function del(id, comment_id) {
    fd = new FormData();
    fd.append('uid', id);
    fd.append('comment_id', comment_id);

    $.ajax({
        url: '/delete/',
        data: fd,
        async: false,
        processData: false,
        contentType: false,
        type: 'POST'
    }).done(function() {
        window.location.reload();
    });
    return false;
}
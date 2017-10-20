blue = false;
red = false;

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

$("#like").click(function () {

    if(!blue){
        $("#like_icon").css("color", "blue");
        blue = true;
        $("#dislike").attr("disabled", true);

        fd = new FormData();
        fd.append("like", "1");

        $.ajax({
            url: '/like_ranking/',
            data: fd,
            processData: false,
            contentType: false,
            type: 'POST',
        });

    }else{
        $("#like_icon").css("color", "dimgrey");
        blue = false;
        $("#dislike").attr("disabled", false);

        fd = new FormData();
        fd.append("like", "-1");

        $.ajax({
            url: '/like_ranking/',
            data: fd,
            processData: false,
            contentType: false,
            type: 'POST',
        });
    }
});

$("#dislike").click(function () {
    if(!red) {
        $("#dislike_icon").css("color", "red");
        red = true;
        $("#like").attr("disabled", true);

        fd = new FormData();
        fd.append("dislike", "1");

        $.ajax({
            url: '/like_ranking/',
            data: fd,
            processData: false,
            contentType: false,
            type: 'POST',
        });

    }else{
        $("#dislike_icon").css("color", "dimgrey");
        red = false;
        $("#like").attr("disabled", false);

        fd = new FormData();
        fd.append("dislike", "-1");

        $.ajax({
            url: '/like_ranking/',
            data: fd,
            processData: false,
            contentType: false,
            type: 'POST',
        });
    }
});
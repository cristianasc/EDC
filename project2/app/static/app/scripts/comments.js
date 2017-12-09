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
        success: function(data){
            location.reload();
      },
      error: function(e) {
          alert(e);
      }
    });

});
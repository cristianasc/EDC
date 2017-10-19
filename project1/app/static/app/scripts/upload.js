//source: http://shinworld.altervista.org/image-upload-form/

function noPreview() {
    $('#image-preview-div').css("display", "none");
    $('#preview-img').attr('src', 'noimage');
    $('upload-button').attr('disabled', '');
}

function selectImage(e) {
    $('#file').css("color", "green");
    $('#image-preview-div').css("display", "block");
    $('#preview-img').attr('src', e.target.result);
    $('#preview-img').css('max-width', '550px');
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var file;

$(document).ready(function (e) {

    var maxsize = 500 * 1024; // 500 KB
    $('#max-size').html((maxsize / 1024).toFixed(2));

    // submit form
    $("#new").submit(function (e) {
        var fd = new FormData();

        if(file==undefined){
            alert("Selecione uma foto!");
        }else{
            fd.append('file', file);
            fd.append('description', $("#description").val());
            fd.append('title', $("#title").val());

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: '/create_new/',
                data: fd,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function (data) {
                    alert("Notícia criada!");
                }
            });
        }

        e.preventDefault();
    });


    $('#file').change(function () {
        $('#message').empty();

        file = this.files[0];
        var match = ["image/jpeg", "image/png", "image/jpg"];

        if (!( (file.type == match[0]) || (file.type == match[1]) || (file.type == match[2]) )) {
            noPreview();

            $('#message').html('<div class="alert alert-warning" role="alert">Unvalid image format. Allowed formats: JPG, JPEG, PNG.</div>');

            return false;
        }

        if (file.size > maxsize) {
            noPreview();

            $('#message').html('<div class=\"alert alert-danger\" role=\"alert\">The size of image you are attempting to upload is ' + (file.size / 1024).toFixed(2) + ' KB, maximum size allowed is ' + (maxsize / 1024).toFixed(2) + ' KB</div>');

            return false;
        }

        $('#upload-button').removeAttr("disabled");

        var reader = new FileReader();
        reader.onload = selectImage;
        reader.readAsDataURL(this.files[0]);

    });

});
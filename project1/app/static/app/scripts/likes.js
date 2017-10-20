
var blue = false;
var red = false;

$("#like").click(function () {

    if(!blue){
        $("#like_icon").css("color", "blue");
        blue = true;
        $("#dislike").attr("disabled", true);;
    }else{
        $("#like_icon").css("color", "dimgrey");
        blue = false;
        $("#dislike").attr("disabled", false);;
    }
});

$("#dislike").click(function () {
    if(!red) {
        $("#dislike_icon").css("color", "red");
        red = true;
        $("#like").attr("disabled", true);;
    }else{
        $("#dislike_icon").css("color", "dimgrey");
        red = false;
        $("#like").attr("disabled", false);;
    }
});
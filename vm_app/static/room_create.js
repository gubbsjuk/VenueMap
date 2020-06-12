function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function() {
    var shape = document.getElementById("id_shape");
    var button = document.createElement("button");
    button.innerHTML = "Rect";
    button.onclick = function() {
        shape.value = "rect";
    }
    document.getElementById("buttonPanel").appendChild(button);

    $("#roomForm").submit(function(e){
        e.preventDefault();
        alert("Submitting!");
        var form = $(this);
        console.log("Form is:");
        console.log(form);

        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $(this).ajaxSubmit({
            url : '/room_create/',
            type : 'POST',
            success : function(response) {
                alert(response);
                updateRoomPKs(response)
            }
        });
    });

    $("#coordForm").submit(function(e){
        e.preventDefault();
        alert("Submitting!");
        var form = $(this);
        console.log("Form is:");
        console.log(form);

        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $(this).ajaxSubmit({
            url : '/room_create_coordinates/',
            type : 'POST',
        });
    });
});

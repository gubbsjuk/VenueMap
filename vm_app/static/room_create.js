function myFunction(sel) {
    text = sel.options[sel.selectedIndex].text;

    req = $.ajax({
        url : '/room_create',
        type : 'GET',
        data : { shape : text }
    });
    req.done(function(data) {
        $('#coordinateSection').fadeOut(0).fadeIn(500);
        $('#coordinateSection').html(data);
    });
}




function updateRoomPKs(pk) {
    var toUpdate = document.querySelectorAll('input[id^="id_form"][id$="room"]');
    alert("updating " + toUpdate.length + "pk's to " + pk);
    for (x of toUpdate) {
        alert(x.id);
        x.value = pk;
    }

    document.getElementById("coordForm").submit();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

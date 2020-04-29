    function myFunction(room) {
        req = $.ajax({
            url : '/room_detail',
            type : 'GET',
            data : { room : room }
        });

        req.done(function(data) {
            $('#activitySection').fadeOut(0).fadeIn(500);
            $('#activitySection').html(data);
        });
    }
$('#id_coordinates').change(function(e) {
    if (e.originalEvent) {
        // user-triggered event
        coordinates = document.getElementById("id_coordinates").value;
        validateCoordinates(coordinates);
    }
})

function validateCoordinates(cString) {
    coordinates = cString.split(',');
    
    var shape = document.getElementById("id_shape").value;

    if (coordinates.length == 4) {
        start = [coordinates[0], coordinates[1]];
        end = [coordinates[2], coordinates[3]];

        if (shape == 'rect') {
            drawRect(start, end[0] - start[0], end[1] - start[1]);
        }
    
        else if (shape == 'circle') {
            drawCircle(start, end);
        }

        else {
            alert("invalid coordinates");
        }
    }

    else {
        alert("invalid coordinates");
    }
}

var canvas = document.getElementById("venueImgCanvas");
var ctx= canvas.getContext("2d");
ctx.lineWidth = 2;

var canvasOffset = $("#venueImgCanvas").offset();
var offsetX = canvasOffset.left;
var offsetY = canvasOffset.top;

var img = new Image();
img.onload = function() {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
}

var startpoint, endpoint, timeout;
var pressed = false;

function degToRad(degrees) {
    return degrees * Math.PI / 180;
}

function drawRect(start, width, height) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);
    ctx.beginPath();
    ctx.rect(start[0], start[1], width, height);
    ctx.stroke();
}

function drawCircle(start, stop) {
    radius = Math.sqrt(Math.pow((stop[0] - start[0]),2) + Math.pow((stop[1] - start [1]),2));
    console.log(radius)

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);
    ctx.beginPath();
    ctx.arc(start[0], start[1], radius, degToRad(0), degToRad(360), false);
    ctx.stroke();
}

$("#venueImgCanvas").mousedown(function (e){
    startpoint = getCursorLoc(e);
    endpoint = getCursorLoc(e);
    var shape = document.getElementById("id_shape").value;
    if (shape) {
        timeout = setInterval(function(){
        pressed = true;
        if (endpoint != null){
            if (shape == 'rect') {
                popCoords(startpoint, endpoint);
                drawRect(startpoint, endpoint[0] - startpoint[0], endpoint[1] - startpoint[1]);
            }
            if (shape == 'circle') {
                popCoords(startpoint, endpoint);
                drawCircle(startpoint, endpoint);
            }
        }
        }, 50);
    }
    return false;
});

$("#venueImgCanvas").mouseup(function (e){
    if (timeout != null) {
        clearInterval(timeout);
    }
    return false;
});

$("#venueImgCanvas").mouseout(function() {
    if (timeout != null) {
        clearInterval(timeout);
    }
    return false;
});

$("#venueImgCanvas").mousemove(function (e){
    if (pressed) {
        endpoint = getCursorLoc(e);
    }
});

function getCursorLoc(e) {
    mouseX = parseInt(e.clientX - offsetX);
    mouseY = parseInt(e.clientY - offsetY);

    return [mouseX, mouseY];
}

function popCoords(startpoint, endpoint) {
    var coordinates = document.getElementById("id_coordinates")
    coordinates.value = startpoint[0] + "," + startpoint[1] + "," + endpoint[0] + "," + endpoint[1];
}

$(document).ready(function() {
    var shape = document.getElementById("id_shape");

    var rectButton = document.createElement("button");
    rectButton.innerHTML = "Rect";
    rectButton.onclick = function() {
        shape.value = "rect";
    }

    var circleButton = document.createElement("button");
    circleButton.innerHTML = "Circle";
    circleButton.onclick = function() {
        shape.value = "circle";
    }

    var btnPanel = document.getElementById("buttonPanel");
    btnPanel.appendChild(rectButton);
    btnPanel.appendChild(circleButton);

});

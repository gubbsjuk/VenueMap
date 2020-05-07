// variable for passing in modulenames from template.
//OPTIMIZE: Can this be removed?
var modulenames;

//create modules
updateModule(1, null, false);
updateModule(2, null, false);

function getModuleNames(data) {
    modulenames = data;
}

//Called by populateModule function
function createModuleSelector(modulePos, data, init) {

    var form = document.createElement("FORM");
    form.className = "float-right"
    form.id = "module"+modulePos+"-form";
    var select = document.createElement("SELECT");
    select.id = "module"+modulePos+"-select";

    data.forEach(function(item) {
        var option = document.createElement("option");
        option.value = item[0];
        option.text = item[1];
        select.add(option);
    });
    form.appendChild(select);
    // Set initial selection
    for(var i, j = 0; i = select.options[j]; j++) {
        if(i.value == init) {
            select.selectedIndex = j;
            break;
        }
    }
    select.onchange = function(e) {
        updateModule(modulePos, select.options[select.selectedIndex].value, true);
    };

    return form;
}

function venueModule(data) {
    // VENUE
    var body = document.createElement("ul");
    data.forEach(function(element){
        if (!element["header"]){
            var li = document.createElement('li');
            var a = document.createElement('a');
            var linkText = document.createTextNode(element["name"]);
            a.appendChild(linkText);
            a.title= element["name"];
            a.href = "/venues/" + element["pk"];
            li.appendChild(a);
            body.appendChild(li);
        }
    });

    return body;
}

function activitiesModule(data, today) {
    var body = document.createElement("TABLE");
    var rooms = [];

    //For loop to get all rooms, and sort them?
    data.forEach(function(element) {
        if(!element["header"]) {
            rooms.push(element["room"]);
        }
    });
    rooms.sort();
    
    //For loop to add all activities under current room to table
    rooms.forEach(function(room){
        var headerRow = document.createElement("tr");
        var header = document.createElement("th");
        var roomtext = document.createTextNode(room);
        header.appendChild(roomtext);
        headerRow.appendChild(header);
        body.appendChild(headerRow);
        data.forEach(function(element){
            if (element["room"] == room) {
                var tablerow = document.createElement("tr");

                var activitydata = document.createElement("td");
                var activitytext = document.createTextNode(element["name"]);
                activitydata.appendChild(activitytext);
                var startDateTime = new Date(element["start"]);

                if (today) {
                    var startText = startDateTime.toLocaleTimeString();
                }
                else {
                    var startText = startDateTime.toDateString() + " - " + startDateTime.toLocaleTimeString();
                }
                
                var datedata = document.createElement("td");
                var datetext = document.createTextNode(startText);
                datedata.appendChild(datetext);

                tablerow.appendChild(activitydata);
                tablerow.appendChild(datedata);

                body.appendChild(tablerow);
            }
        });
    });

    return body;
}

//TODO: Implement URLs to rooms.
function roomsModule(data) {
    var body = document.createElement("ul");

    data.forEach(function(element){
        if (!element["header"]){
            var li = document.createElement('li');
            var a = document.createElement('a');
            var linkText = document.createTextNode(element["name"]);
            a.appendChild(linkText);
            a.title= element["name"];
            a.href = "/rooms/" + element["pk"];
            li.appendChild(a);
            body.appendChild(li);
        }
    });
    return body;
}

//TODO: Implement tocleanModule
function tocleanModule(data) {
    var body = document.createElement("ul");

    return body;
}

//Called by updateModule function
function populateModule(modulePos, data) {
    var divHeader = document.getElementById("module"+modulePos+"-header");
    var divBody = document.getElementById("module"+modulePos+"-body");
    var header = document.createElement("H5");
    var headertext;
    
    // Clear existing content of module
    divHeader.innerHTML = "";
    divBody.innerHTML = "";

    var moduletype;
    if (data[0]) {
        moduletype = data[0]["header"];
        if (moduletype == 1) { // VENUE
            headertext = document.createTextNode("My Venues:");
            divBody.appendChild(venueModule(data));
        }
        if (moduletype == 2) { // ACTIVITIES
            headertext = document.createTextNode("Upcoming Activities:");
            divBody.appendChild(activitiesModule(data, false));
        }
        if (moduletype == 3) { // TODAY
            headertext = document.createTextNode("Activities today:");
            divBody.appendChild(activitiesModule(data, true));
        }
        if (moduletype == 4) { // ROOMS
            headertext = document.createTextNode("My Rooms:");
            divBody.appendChild(roomsModule(data));
        }
        if (moduletype == 5) { // TOCLEAN
            headertext = document.createTextNode("Rooms to be cleaned:");
            divBody.appendChild(tocleanModule(data));
        }
    }
    header.appendChild(headertext);
    header.appendChild(createModuleSelector(modulePos, modulenames, moduletype));
    divHeader.appendChild(header);
}

//Defining wich request to implement csrf-token on.
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//Function to update or generate modules.
//modulePos = int
//module = modulename.pk
//update = true / false
function updateModule(modulePos, module, update) {
    var csrftoken = getCookie('csrftoken');

    if (!update) {
        module = null;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    req = $.ajax({
        url : '/',
        type : 'POST',
        data : {
            modulePos : modulePos,
            module : module,
            update : update,
        }
    });

    req.done(function(data) {
        populateModule(modulePos, data);
    });
}


// Cookie functions not currently in use. Grabbing from db instead.
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length,c.length);
        }
    }
    return "";
}
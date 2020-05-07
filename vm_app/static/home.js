// Cookie functions not currently in use. Grabbing from db instead.
var modulenames;

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

createModule(1);
createModule(2);

function createModule(modulePos) {
    getModules(modulePos);
}

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
        updateModule(modulePos, select.options[select.selectedIndex].value);
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
            a.href = "/venue/" + element["pk"];
            li.appendChild(a);
            body.appendChild(li);
        }
    });

    return body;
}

function todayModule(data) {
    var body = document.createElement("ul");
    data.forEach(function(element){
        if (!element["header"]) {
            var li = document.createElement('li');
            var a = document.createElement('a');
            var linkText = document.createTextNode(element["name"]);
            var start = document.createTextNode(element["start"]);
            a.appendChild(linkText);
            a.title = element["name"];
            a.href = "/activites/" + element["pk"];
            li.appendChild(a);
            li.appendChild(start);
            body.appendChild(li);
        }
    });
    
    return body;
}

//TODO: Implement filtering by room on activites. Should also filter out expired activities.
function activitiesModule(data) {
    var body = document.createElement("ul");
    data.forEach(function(element){
        if (!element["header"]) {
            var li = document.createElement('li');
            var a = document.createElement('a');
            var linkText = document.createTextNode(element["name"]);
            var start = document.createTextNode(element["start"]);
            a.appendChild(linkText);
            a.title = element["name"];
            a.href = "/activites/" + element["pk"];
            li.appendChild(a);
            li.appendChild(start);
            body.appendChild(li);
        }
    });
    return body;
}

//TODO: Implement roomModule
function roomsModule(data) {
    var body = document.createElement("ul");

    return body;
}

//TODO: Implement tocleanModule
function tocleanModule(data) {
    var body = document.createElement("ul");

    return body;
}

//Called by sendGet function
//Optimize: Segment out different views.
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
            divBody.appendChild(activitiesModule(data));
        }
        if (moduletype == 3) { // TODAY
            headertext = document.createTextNode("Activities today:");
            divBody.appendChild(todayModule(data));
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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function updateModule(modulePos, module) {
    var csrftoken = getCookie('csrftoken');

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
            module : module 
        }
    });

    req.done(function(data) {
        populateModule(modulePos, data);
    });
}

//TODO: Change this to POST?
function getModules(modulePos) {
    req = $.ajax({
        url : '/',
        type : 'GET',
        data : {
                modulePos : modulePos
            }
    });
    req.done(function(data) {
        populateModule(modulePos, data);
    });
}

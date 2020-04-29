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

createModule(1);
createModule(2);

function createModule(modulePos) {
    sendGET(modulePos);
}

function populateModule(modulePos, data) {
    console.log(data);
    var divModule = document.getElementById("module"+modulePos);
    var divHeader = document.createElement("div");
    var header = document.createElement("H5");
    var headertext;
    var divBody = document.createElement("div");
    var body = document.createElement("ul");

    var moduletype;
    data.forEach(function(element){
        if (element["header"]){
            moduletype = element["header"]
            if (moduletype == "venue") {
                headertext = document.createTextNode("My Venues:");
            }
            if (moduletype == "today") {
                headertext = document.createTextNode("Activities today:");
            }

        } else {
            if (moduletype == "venue") {
                var li = document.createElement('li');
                var a = document.createElement('a');
                var linkText = document.createTextNode(element["name"]);
                a.appendChild(linkText);
                a.title= element["name"];
                a.href = "/venue/" + element["pk"];
                li.appendChild(a);
                body.appendChild(li);
            }

            if (moduletype == "today") {
                var li = document.createElement('li');
                var a = document.createElement('a');
                var linkText = document.createTextNode(element["name"]);
                a.appendChild(linkText);
                a.title = element["name"];
                a.href = "/activites/" + element["pk"];
                li.appendChild(a);
                body.appendChild(li);
            }
        }
    })

    divBody.appendChild(body);
    divBody.className = "card-body";
    header.appendChild(headertext);
    divHeader.appendChild(header);
    divHeader.className = "card-header";
    divModule.appendChild(divHeader);
    divModule.appendChild(divBody);
}

function sendGET(modulePos) {
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


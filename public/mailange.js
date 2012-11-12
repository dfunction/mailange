var request, targetDiv, requestData;

function ajaxRequest(){
    var activexmodes=["Msxml2.XMLHTTP", "Microsoft.XMLHTTP"]; //activeX versions to check for in IE
    if (window.ActiveXObject){ //Test for support for ActiveXObject in IE first (as XMLHttpRequest in IE7 is broken)
        for (var i=0; i<activexmodes.length; i++){
            try{
                return new ActiveXObject(activexmodes[i]);
            }
            catch(e){
            //suppress error
            }
        }
    }
    else if (window.XMLHttpRequest) // if Mozilla, Safari etc
        return new XMLHttpRequest();
    else
        return false
}

function handleChange() {
    if (request.readyState==4 && request.status == 200){
        var response=eval("("+request.responseText+")"); //retrieve result as an JavaScript object
        targetDiv.innerHTML = response.email;
        var head= document.getElementsByTagName('head')[0];
        var style = document.createElement("style");
        style.innerHTML = "@font-face{font-family: 'mailange';src: url('data:font/opentype;base64," + response.font + "') format('svg');}";
        head.appendChild(style);
        targetDiv.style.fontFamily = "mailange";
    }
    else if (request.readyState == 4){
        console.log("An error has occured making the request");
    }
}

(function main() {
    request = new ajaxRequest();
    request.onreadystatechange = handleChange;
    targetDiv = document.getElementById("mailange");
    requestData = new FormData();

    requestData.append("hash", targetDiv.getAttribute("data-hash"));
    request.open("POST", "http://mailange.juanolivar.com/retrieve", true);
    request.send(requestData);
})();

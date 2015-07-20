function loadFrame(){
    var targetUrl = document.getElementById('targetURL').value;
    document.getElementById('victimFrame').src=targetUrl;
}

function sendMessageToFrame(){
    var url = document.getElementById('targetURL').value;
    var message = document.getElementById('message').value;
    appendToConsole("Sending: " + message + " to: "+ url);
    var attackFrame = document.getElementById("attackFrame");
    attackFrame.contentWindow.postMessage(message, url);

}

function appendToConsole(newLogMessage){
    var logMessage = document.getElementById('console').innerHTML.toString();
    if (logMessage.length > 6){
        logMessage = logMessage + "<br/>"
    }
    logMessage = logMessage + newLogMessage;
    document.getElementById('console').innerHTML = logMessage;
}

function setCurrentDomain(){
    var curDomain = document.getElementById('curDomain').value;
    var attackFrame = document.getElementById('attackFrame');
    attackFrame.src = curDomain;
}

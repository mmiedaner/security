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

function registerEventHandler(){
    var frame = document.createElement('iframe');
    var head = document.createElement('head');
    var body = document.createElement('body');
    var script = document.createElement('script');
    script.innerHTML='function msgReceiver(event){ alert(event.data); }; window.addEventListener(\'message\', msgReceiver, false);';
    body.appendChild(script);
    frame.appendChild(head);
    frame.appendChild(body);
    document.getElementById('victimFrame')=frame;
}

function setCurrentDomain(){
    var curDomain = document.getElementById('curDomain').value;
    var attackFrame = document.getElementById('attackFrame');
    attackFrame.src = curDomain;
}
var pmat = {

    loadFrames: function(){
        var targetUrl = $('#targetURL').val();
        $('#victimFrame').attr('src',targetUrl);
        var attackURL = $('#attackURL').val();
        var attackFrame = $('#attackFrame');
        attackFrame.attr('src', attackURL);
    },

    sendMessageToFrame: function(){
        var url = $('#targetURL').val();
        var message = $('#message').val();
        this.appendToConsole("Sending: " + message + " to: "+ url);

        var attackFrame = $("#attackFrame").get(0);
        if (attackFrame != undefined){
            attackFrame.contentWindow.postMessage(message, url);
        }
        else{
            this.contentWindow.postMessage(message, url);
        }
    },

    appendToConsole: function(newLogMessage){
        var logMessage = $('#console').html().toString();
        if (logMessage.length > 6){
            logMessage = logMessage + "<br/>"
        }
        logMessage = logMessage + newLogMessage;
        $('#console').html(logMessage);
    },

<<<<<<< HEAD:pmat/js/pmat.js
    setCurrentDomain: function(){
    }
}
=======
function setCurrentDomain(){
    var curDomain = document.getElementById('curDomain').value;
    var attackFrame = document.getElementById('attackFrame');
    attackFrame.src = curDomain;
}
>>>>>>> f5c5a0e558cf370e742f6c9256a7bc75667c22eb:pmat2/js/pmat.js

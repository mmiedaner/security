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

    setCurrentDomain: function(){
    }
}
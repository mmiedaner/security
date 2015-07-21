var pmat = {

    loadFrame: function(frame){
        if (frame == "victim"){
            var targetUrl = $('#targetURL').val();
            $('#victimFrame').attr('src',targetUrl);
        }
        else{
            var attackURL = $('#attackURL').val();
            $('#attackFrame').attr('src', attackURL);
        }
    },

    sendMessage: function(frame){
        var url = $('#targetURL').val();
        var message = $('#message').val();
        this.appendToConsole("Sending: " + message + " to: "+ url + " from: " + frame + " frame");

        var attackFrame = $("#attackFrame").get(0);
        if (frame == "attack"){
            attackFrame.contentWindow.postMessage(message, url);
        }
        else{
            $('#internalIFrame').get(0).contentWindow.postMessage(message, url);
        }
    },

    appendToConsole: function(newLogMessage){
        var logMessage = $('#console').html().toString();
        if (logMessage.length > 6){
            logMessage = logMessage + "<br/>"
        }
        logMessage = logMessage + newLogMessage;
        $('#console').html(logMessage);
    }
}
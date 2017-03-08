
// ----------
// AJAX Setup
// ----------
var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') 
    {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) 
        {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) 
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

$.ajaxSetup({
    beforeSend: function(xhr, settings) 
    {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) 
        {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};
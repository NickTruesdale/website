
 
// Add click handlers when the page loads
$(function() {
    // Capture modal button click and initial load
    $('.modal-button').click(modalPreload);
    $('#modalForm').on('show.bs.modal', modalLoad);

    // Click handlers for dynamically generated elements
    $(document).on('click', '.form-submit', formSubmitHandler);
});

// When a modal button is clicked, pass that button's URL over to the 
// modal window so it knows which form to get
var modalPreload = function()
{
    targetUrl = $(this).attr('data-url');
    $('#modalForm').attr('data-url', targetUrl);
};

// GET the form for the modal window on load
var modalLoad = function() 
{
    var modal = $(this);
    $.ajax({
        url: modal.attr('data-url'),
        context: document.body,
        success: function(data) {
            modal.html(data);
        }
    });   
};

// This is the form submission AJAX POST for all of the modal forms
var formSubmitHandler = function() 
{
    var key, idx, listItem, message;
    var form = $(this).closest("form");
    var postUrl = form.attr('action');

    // Submit POST via ajax and process the response
    $.ajax({
        type: "POST",
        dataType: "json",
        url: postUrl,
        data: form.serialize(),

        success: function(data) {
            console.log(data);

            // Clear error formatting
            $('.field-errors').empty();
            $('.field-errors').removeClass('alert alert-danger');

            // Place the response next to the submit button
            $('.form-response').removeClass('alert alert-danger alert-success');
            $('.form-response').text(data.message);
            
            // Check whether the form was valid or invalid
            if (data.success)
            {
                $('#modalForm').html('');
                $('#modalForm').modal('hide');
            }
            else
            {   
                // Diaply an error message
                message = 'Object could not be ';
                message += ($('.form-pk').text() === 'None') ? 'created' : 'updated';
                message += '. Please resolve any errors and submit again.' ;
                $('.form-response').text(message);
                $('.form-response').addClass('alert alert-danger');
                
                // Add errors to each affected field
                for (key in data.errors)
                {
                    for (idx=0; idx < data.errors[key].length; idx++)
                    {
                        listItem = '<li>' + data.errors[key][idx] + '</li>';
                        $('#field-errors-' + key).append(listItem);
                        $('#field-errors-' + key).addClass('alert alert-danger');
                    } 
                }
            }
        },

        error: function(xhr, errmsg, err) {
            console.log(xhr);
            console.log(errmsg);
            console.log(err);
        },
    });
};

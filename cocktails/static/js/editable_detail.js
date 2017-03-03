
// Page initialization (before document ready)
var initialize = function() 
{
    // Set editable fields to hidden
    $('.editable-field, .editable-button').addClass('hide');

    // Show the page
    $('.page-wrapper').removeClass('hide');
};

// Click handler for the submit button
var detailSubmitHandler = function()
{
    // Prepare vars
    var form = $(this).closest('form');
    var postUrl = form.attr('action');

    // Ajax POST
    $.ajax({
        type: "POST",
        dataType: "json",
        url: postUrl,
        data: form.serialize(),

        success: function(data) {
            // Clear error formatting
            $('.field-errors').empty();
            $('.field-errors').removeClass('alert alert-danger');

            // If successful, return to detail mode and save new data to form
            if (data.success)
            {
                makeReadOnly();
                $('.readonly-field').each(copyFromEditable);
            }

            // Otherwise, display error messages
            else
            {   
                // Add errors to each affected field
                for (var key in data.errors)
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
    });
};

// Click handler for the edit button. 
var detailEditHandler = function()
{
    // convert fields to edit mode
    $('.derived').addClass('hide');
    $('.readonly-field').addClass('hide');
    $('.editable-field, .editable-button').removeClass('hide');

    // Enable the submit and cancel buttons
    $('#detail-submit-button, #detail-cancel-button').removeClass('hide');
    $('#detail-edit-button').addClass('hide');

    // Change the image to a URLField
    $('#detail-image-panel').addClass('panel panel-default');
    $('#detail-image-header').removeClass('hide');
    $('#detail-image-edit').removeClass('hide');
};

// Click handler for the cancel button
var detailCancelHandler = function()
{
    // Convert everything back to readonly mode
    makeReadOnly();

    // Copy original data from readonly elements back into editable ones
    $('.editable-field').each(copyFromReadonly);

    // Clear any errors that were generated
    $('.field-errors').empty();
    $('.field-errors').removeClass('alert alert-danger');
};

// Hide all editable fields and return to readonly mode
var makeReadOnly = function() 
{
    // convert fields to readonly mode
    $('.derived').removeClass('hide');
    $('.readonly-field').removeClass('hide');
    $('.editable-field, .editable-button').addClass('hide');

    // Hide the submit and cancel buttons
    $('#detail-submit-button, #detail-cancel-button').addClass('hide');
    $('#detail-edit-button').removeClass('hide');

    // Remove image edit fields
    $('#detail-image-panel').removeClass('panel panel-default');
    $('#detail-image-header').addClass('hide');
    $('#detail-image-edit').addClass('hide');
};

// Applied to a field with the readonly-field class, this will find its
// corresponding editable field and copy the value over to it
var copyFromReadonly = function()
{
    var id = '#' + $(this).attr('id');
    var srcId = id.replace('id', 'readonly');
    var elementType = $(this).get(0).tagName.toLowerCase();

    // For normal fields, we can just copy the text
    if (elementType === 'input' || elementType === 'textarea')
    {
        $(id).val($(srcId).text());
    }
    // For select fields, we need to copy the ID instead of the value 
    else if (elementType === 'select')
    {
        $(id).val($(srcId).attr('data-pk'));
    }
};

// Applied to a field with the editable-field class, this will find its
// corresponding readonly field and copy the value over to it
var copyFromEditable = function()
{
    var id = '#' + $(this).attr('id');
    var srcId = id.replace('readonly', 'id');
    var pk = $(this).attr('data-pk');

    // Only select fields have the data-pk parameter, which stores the ID used in 
    // the foreign key select so we can access the name of that object
    if (pk)
    {
        console.log(pk);
        pk = $(srcId).val();
        $(id).attr('data-pk', pk);
        $(id).text($(srcId + " option[value='" + pk + "']").text());
    }
    // For all other field types, we can just copy the value
    else
    {
        $(id).text($(srcId).val());
    }
};

// Add click handlers when the page loads
$(function() {
    // Initialize the page
    initialize();

    // Edit, Submit and Cancel handlers
    $('#detail-edit-button').click(detailEditHandler);
    $('#detail-submit-button').click(detailSubmitHandler);
    $('#detail-cancel-button').click(detailCancelHandler);
});
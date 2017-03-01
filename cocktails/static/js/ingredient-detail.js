
// Page initialization (before document ready)
var initialize = function() 
{
    // Set editable fields to hidden
    $('.editable-field, .editable-button').addClass('hide');

    // Show the page
    $('.page-wrapper').removeClass('hide');
};

// Click handler for the edit button. 
var ingredientEditHandler = function()
{
    // convert fields to edit mode
    $('.readonly-field').addClass('hide');
    $('.editable-field, .editable-button').removeClass('hide');

    // Enable the submit and cancel buttons
    $('#ingredient-submit-button, #ingredient-cancel-button').removeClass('hide');
    $('#ingredient-edit-button').addClass('hide');

    // Change the image to a URLField
    $('#ingredient-image-panel').addClass('panel panel-default');
    $('#ingredient-image-header').removeClass('hide');
    $('#ingredient-image-edit').removeClass('hide');
};

var ingredientSubmitHandler = function()
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

    // Convert everything back to readonly mode
    
};

var ingredientCancelHandler = function()
{
    // Convert everything back to readonly mode
    makeReadOnly();

    // Copy original data from readonly elements back into editable ones
    $('.editable-field').each(copyFromReadonly);

    // Clear any errors that were generated
    $('.field-errors').empty();
    $('.field-errors').removeClass('alert alert-danger');
};

var makeReadOnly = function() 
{
    // convert fields to readonly mode
    $('.readonly-field').removeClass('hide');
    $('.editable-field, .editable-button').addClass('hide');

    // Hide the submit and cancel buttons
    $('#ingredient-submit-button, #ingredient-cancel-button').addClass('hide');
    $('#ingredient-edit-button').removeClass('hide');

    // Remove image edit fields
    $('#ingredient-image-panel').removeClass('panel panel-default');
    $('#ingredient-image-header').addClass('hide');
    $('#ingredient-image-edit').addClass('hide');
};

var copyFromReadonly = function()
{
    var id = '#' + $(this).attr('id');
    var srcId = id.replace('id', 'readonly');
    var elementType = $(this).get(0).tagName.toLowerCase();

    if (elementType === 'input' || elementType === 'textarea')
    {
        $(id).val($(srcId).text());
    }
    else if (elementType === 'select')
    {
        $(id).val($(srcId).attr('data-pk'));
    }
};

var copyFromEditable = function()
{
    var id = '#' + $(this).attr('id');
    var srcId = id.replace('readonly', 'id');
    var pk = $(this).attr('data-pk');

    if (pk)
    {
        console.log(pk);
        pk = $(srcId).val();
        $(id).attr('data-pk', pk);
        $(id).text($(srcId + " option[value='" + pk + "']").text());
    }
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
    $('#ingredient-edit-button').click(ingredientEditHandler);
    $('#ingredient-submit-button').click(ingredientSubmitHandler);
    $('#ingredient-cancel-button').click(ingredientCancelHandler);
});
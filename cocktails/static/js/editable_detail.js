
// Globals
var cancelFlag = false;


// Page initialization (before document ready)
var initialize = function() 
{
    // Get the URL string so we can parse it for initial state
    var url = window.location.pathname;

    // Set up the page depending on whether we are making a new item,
    // editing one or just viewing one
    if (url.includes('new') || url.includes('edit'))
    {
        makeEditable();
    }
    else
    {
        makeReadonly();
    }

    // Show the page
    $('.page-wrapper').removeClass('hide');

    // Edit, Submit and Cancel handlers
    $('#detail-edit-button').click(detailEditHandler);
    $('#detail-submit-button').click(detailSubmitHandler);
    $('#detail-cancel-button').click(detailCancelHandler);

    // Field change handlers
    $('#id_image_url').change(function(){ $('#id_image').attr('src', $(this).val()); });
    $('#id_country').change(showHideUSState);

    $('#id_ingredient_class').change(ingredientClassChange);
    $('#id_ingredient_category').change(ingredientCategoryChange);

    // Trigger change events on load
    $('#id_country').change();
    //$('#id_ingredient_class').change();
};

// Click handler for the submit button
var detailSubmitHandler = function()
{
    // Prepare vars
    var form = $(this).closest('form');
    var postUrl = form.attr('action');

    // Make sure category and subcategory are not disabled
    if ($('#id_ingredient_category, #id_subcategory').prop('disabled') === true)
    {
        listItem = $('<li>', {text: 'All three categorization levels must be filled out.'});
        $('#field-errors-subcategory').append(listItem);
        $('#field-errors-subcategory').addClass('alert alert-danger');
        return;
    }

    // Ajax POST
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

            // If successful, return to detail mode and save new data to form
            if (data.success)
            {
                makeReadonly();
                $('.readonly-field').each(copyFromEditable);

                if (window.location.pathname.includes('new'))
                {
                    window.history.back();
                }
                else
                {
                    window.history.replaceState({}, 'Detail', data.detail_url);
                }
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
    // Switch to editable mode and upadte the URL to say we're editing
    makeEditable();
    window.history.replaceState({}, 'Edit', 'edit/');
};

// Click handler for the cancel button
var detailCancelHandler = function()
{
    // Either return to detail or exit the page
    if (window.location.pathname.includes('new'))
    {
        window.history.back();
    }
    else
    {
        // Switch to readonly mode and remove edit from the URL
        makeReadonly();
        window.history.replaceState({}, 'Detail', window.location.pathname.replace('edit/', ''));

        // Copy original data from readonly elements back into editable ones
        $('.editable-field').each(copyFromReadonly);
           
        // Explicitly call the change handler for the class, which will cascade and
        // update the category and subcategory 
        copyCategorizationFromReadonly();

        // Clear any errors that were generated
        $('.field-errors').empty();
        $('.field-errors').removeClass('alert alert-danger');
    }
};

// Hide the readonly and derived fields and show the form
var makeEditable = function()
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

// Hide all editable fields and return to readonly mode
var makeReadonly = function() 
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

// The ingredient categories require special handling
var copyCategorizationFromReadonly = function()
{
    var readonlyClass = $('#readonly_ingredient_class').attr('data-pk');
    var readonlyCategory = $('#readonly_ingredient_category').attr('data-pk');
    var readonlySubcategory = $('#readonly_subcategory').attr('data-pk');

    $('id_ingredient_class').val(readonlyClass);
    changeCategorizationOptions(readonlyClass, readonlyCategory, readonlySubcategory);

    if (readonlyCategory) $('#id_ingredient_category').prop('disabled', false);
    if (readonlySubcategory) $('#id_subcategory').prop('disabled', false);
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

// If there is a US State field, bind its visibility to the country field
var showHideUSState = function() {
    var country = $(this).val();

    if (country === 'US')
    {
        $('#field-wrapper-us_state').removeClass('hide');
    }
    else
    {
        $('#id_us_state').val('');
        $('#field-wrapper-us_state').addClass('hide');
    }
};

// Change event handler for the ingredient class select
var ingredientClassChange = function()
{
    var ingredientClass = $(this).val();

    // Clear and disable the subcategory field
    $('#id_subcategory').val('');
    $('#id_subcategory').prop('disabled', true);

    if (ingredientClass === "")
    {
        // Clear and disable the category field
        $('#id_ingredient_category').val('');
        $('#id_ingredient_category').prop('disabled', true);
    }
    else
    {
        // Enable the category field and get the list for this class
        $('#id_ingredient_category').prop('disabled', false);
        changeCategorizationOptions(ingredientClass, null, null);
    }
};

// Change event handler for the ingredient class select
var ingredientCategoryChange = function()
{
    var ingredientClass = $('#id_ingredient_class').val();
    var ingredientCategory = $(this).val();

    if (ingredientCategory === "")
    {
        // Clear and disable the subcategory field
        $('#id_subcategory').val('');
        $('#id_subcategory').prop('disabled', true);
    }
    else
    {
        // Enable the subcategory field and update the list
        $('#id_subcategory').prop('disabled', false);
        changeCategorizationOptions(ingredientClass, ingredientCategory, null);
    }
};

// Change the categorization options given a class and, optionally, a category. 
// The values of filterCategory and setSubcategory will be set into their select fields
var changeCategorizationOptions = function(filterClass, filterCategory, setSubcategory)
{
    $.ajax({
        url: window.location.pathname,
        data: {'filter_class': filterClass, 'filter_category': filterCategory},

        success: function(data) {
            // Update the category list
            $('#id_ingredient_category option').remove();
            for (var idx=0; idx < data.category_options.length; idx++)
            {
                $('#id_ingredient_category').append($('<option>', {
                    value: data.category_options[idx].value, 
                    text: data.category_options[idx].text
                }));
            }

            // If a category was also passed, make sure to set it and update the subcategory list
            if (filterCategory)
            {
                // Update the subcategory list
                $('#id_subcategory option').remove();
                for (idx=0; idx < data.subcategory_options.length; idx++)
                {
                    $('#id_subcategory').append($('<option>', {
                        value: data.subcategory_options[idx].value, 
                        text: data.subcategory_options[idx].text
                    }));
                }

                // Update values in both (if they are null the value will default to empty)
                $('#id_ingredient_category').val(filterCategory);
                $('#id_subcategory').val(setSubcategory);
            }
        },
    });
};

// Add click handlers when the page loads
$(function() {
    initialize();
});
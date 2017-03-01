
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
    // Convert everything back to readonly mode
    makeReadOnly();

    // Copy new data into readonly elements
};

var ingredientCancelHandler = function()
{
    // Convert everything back to readonly mode
    makeReadOnly();

    // Copy original data from readonly elements back into editable ones
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

// Add click handlers when the page loads
$(function() {
    // Initialize the page
    initialize();

    // Edit, Submit and Cancel handlers
    $('#ingredient-edit-button').click(ingredientEditHandler);
    $('#ingredient-submit-button').click(ingredientSubmitHandler);
    $('#ingredient-cancel-button').click(ingredientCancelHandler);
});
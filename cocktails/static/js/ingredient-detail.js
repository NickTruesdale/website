
// Add click handlers when the page loads
$(function() {

    // Edit, Submit and Cancel handlers
    $('#ingredient-edit-button').click(ingredientEditHandler);
    $('#ingredient-submit-button').click(ingredientSubmitHandler);
    $('#ingredient-cancel-button').click(ingredientCancelHandler);
});

var ingredientEditHandler = function()
{
    // Make all fields editable
    $('.no-edit').removeClass('no-edit');

    // Swap the text and selects for the ChoiceFields
    $('.choice-container p').addClass('hide');
    $('.choice-container select').prop('disabled', false);

    // Make the normal fields (input and textfield) not readonly
    $('.text-field').prop('readonly', false);

    // Show the new item icons for each ModelChoiceField
    

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

};

var ingredientCancelHandler = function()
{
    makeReadOnly();
};

var makeEditable = function()
{

};

var makeReadOnly = function() 
{
    // Make all fields editable
    $('.text-field, .select-field, .ingredient-description').addClass('no-edit');

    // Swap the text and selects for the ChoiceFields
    $('.choice-container p').removeClass('hide');
    $('.choice-container select').prop('disabled', true);

    // Make the normal fields (input and textfield) not readonly
    $('.text-field').prop('readonly', true);

    // Hide the submit and cancel buttons
    $('#ingredient-submit-button, #ingredient-cancel-button').addClass('hide');
    $('#ingredient-edit-button').removeClass('hide');

    // Remove image edit fields
    $('#ingredient-image-panel').removeClass('panel panel-default');
    $('#ingredient-image-header').addClass('hide');
    $('#ingredient-image-edit').addClass('hide');
};
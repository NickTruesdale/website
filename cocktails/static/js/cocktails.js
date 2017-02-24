
// 

$(function() {
    // Add click handler for clicked hierarchy titles
    $('.hierarchy-item').click(hierarchyClickHandler);

    // Capture modal button click and initial load
    $('.modal-button').click(modalPreload);
    $('#modalForm').on('show.bs.modal', modalLoad);

    // Click handlers for dynamically generated elements
    $(document).on('click', '.form-submit', formSubmitHandler);
});

var modalPreload = function()
{
    targetUrl = $(this).attr('data-url');
    $('#modalForm').attr('data-url', targetUrl);
};

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

var modalAfterLoad = function()
{
    console.log('shown');
    $('.form-submit').click(formSubmitHandler);
};

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

var hierarchyClickHandler = function() 
{
    // Parse out the model and the pk
    var id = $(this).attr("id");
    var modelType = id.split('-')[0];
    var pk = id.split('-')[1];

    $.ajax({
        url: '/ingredient_categorization/',
        data: {'model_type': modelType, 'pk': pk},

        success: function(data) {
            data = data[0];
            console.log(data);
            var createUrl;

            // Construct the correct edit url for this model and add to the edit button
            // Right now we'll grab this from the create buttons, which is a bit janky
            // and may need to be refactored if we ever remove those buttons.
            var editUrl = $('#modal-create-'+modelType).attr('data-url').replace('new', pk + '/edit');
            $('#modal-edit').attr('data-url', editUrl);

            // Unhide the details panel
            $('.details').show();

            // Fill in the fields
            $('#detail-name span').text(data.fields.name);
            $('#detail-name small').text(modelType.replace('Ingredient',''));
            $('#detail-description').text(data.fields.description);
            $('#detail-wiki').attr('href', data.fields.wiki_url);
            //$('#detail-image').attr('src', data.fields.image_url);

            // Model specific actions
            if (modelType === 'IngredientClass')
            {
                $('#detail-class').hide();
                $('#detail-category').hide();
                $('#modal-create-child').show();

                createUrl = $('#modal-create-IngredientCategory').attr('data-url');
                createUrl += '?class=' + pk;
                $('#modal-create-child').attr('data-url', createUrl);
            }
            else if (modelType === 'IngredientCategory')
            {
                $('#detail-class').text('Parent Class: ' + getParentClass(id));
                $('#detail-class').show();

                $('#detail-category').hide();
                $('#modal-create-child').show();

                createUrl = $('#modal-create-IngredientSubcategory').attr('data-url');
                createUrl += '?category=' + pk;
                $('#modal-create-child').attr('data-url', createUrl);
            }
            else
            {
                $('#detail-class').text('Parent Class: ' + getParentClass(id));
                $('#detail-class').show();

                $('#detail-category').text('Parent Category: ' + getParentCategory(id));
                $('#detail-category').show();

                $('#modal-create-child').hide();
            }
        },

        error: function(xhr, errmsg, err) {
            console.log(xhr);
            console.log(errmsg);
        },
    });
};

var getHierarchyItemName = function(modelType, pk)
{
    var id = '#' + modelType + '-' + pk;
    var name = '';
    var hierarchyItem = $(id);

    if (hierarchyItem.length > 0) name = hierarchyItem.text();
    return name;
};

var getParentClass = function(id)
{
    return $('#' + id).closest('.class-item').find('.hierarchy-item:first').text();
};

var getParentCategory = function(id)
{
    return $('#' + id).closest('.category-item').find('.hierarchy-item:first').text();
};


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
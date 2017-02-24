
// 

$(function() {
    $('.hierarchy-item').click(hierarchyClickHandler);

    //$('.modal-button').click(modalPreload);
    //$('#modal').on('show.bs.modal', modalLoad);
    $('.form-submit').click(formSubmitHandler);
});

var modalPreload = function()
{
    console.log($(this).attr("href"));
};

var modalLoad = function() 
{
    $.ajax({
        url: '/ingredient_class/new/',
        context: document.body,
        success: function(data) {
            $(this).html(data);
        }
    });
};

var formSubmitHandler = function() 
{
    var key, idx, listItem, message;
    var form = $(this).closest("form");
    var postUrl = window.location.pathname;

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
                // Display a success message
                message = 'Object was ';
                message += ($('.form-pk').text() === 'None') ? 'created' : 'updated';
                message += ' successfully.';
                $('.form-response').text(data.message);
                $('.form-response').addClass('alert alert-success');

                // Update the form's pk and change the title
                $('.form-pk').text(data.pk);
                $('.form-header h1:first').text('Update Ingredient Class');
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
    var id = $(this).attr("id");
    var modelType = id.split('-')[0];
    var pk = id.split('-')[1];

    $.ajax({
        url: '/ingredient_categorization/',
        data: {'model_type': modelType, 'pk': pk},

        success: function(data) {
            data = data[0];
            console.log(data);

            $('.details').removeClass('nodisp');

            $('#detail-name').text('Name: ' + data.fields.name);
            $('#detail-description').text('Description: ' + data.fields.description);
            $('#detail-wiki').attr('href', data.fields.wiki_url);
            $('#detail-image').attr('src', data.fields.image_url);

            // If the parent class exists, update it and show the element. Otherwise hide it.
            if (modelType === 'IngredientCategory' || modelType === 'IngredientSubcategory')
            {
                $('#detail-class').text('Parent Class: ' + getParentClass(id));
                $('#detail-class').show();
            }
            else
            {
                $('#detail-class').hide();
            }

            // If the parent category exists, update it and show the element. Otherwise hide it. 
            if (modelType === 'IngredientSubcategory')
            {
                $('#detail-category').text('Parent Category: ' + getParentCategory(id));
                $('#detail-category').show();
            }
            else
            {
                $('#detail-category').hide();
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
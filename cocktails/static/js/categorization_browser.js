
// Add click handlers when the page loads
$(function() {
    // Add click handler for clicked hierarchy titles
    $('.hierarchy-item').click(hierarchyClickHandler);
});

// Load an ingredient class, category or subcategory object when one of these is
// clicked in the categorization browser page.
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

// Return the name of a class given its ID
var getParentClass = function(id)
{
    return $('#' + id).closest('.class-item').find('.hierarchy-item:first').text();
};

// Return the name of a category given its ID
var getParentCategory = function(id)
{
    return $('#' + id).closest('.category-item').find('.hierarchy-item:first').text();
};

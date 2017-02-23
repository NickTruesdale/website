
// 

$(function() {
    $('.hierarchy-item').click(hierarchyClickHandler);
});


var hierarchyClickHandler = function() 
{
    var id = $(this).attr("id");
    var modelType = id.split('-')[0];
    var pk = id.split('-')[1];

    $.ajax({
        url: "/ingredient_categorization/",
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
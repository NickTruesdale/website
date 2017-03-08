
// Add click handlers when the page loads
$(function() {
    // Add handler for ingredient search buttons
    $('.search-button').click(searchHandler);
});

// Make a server call with the search information, and process the list of 
// search results that is returned
var searchHandler = function()
{
    var idx, div, pk, fields;
    var modelType = $(this).attr('data-model');
    var searchText = $(this).parent().find('input:first').val().trim();

    $.ajax({
        url: window.location.pathname,
        data: {'model': modelType, 'search_text': searchText},

        success: function(data) {
            console.log(data);

            // Un-hide the results and hide the "About the site" section
            $('.results-container').html('');
            $('.search-panel').show();
            $('.about-panel').hide();

            // If there were no results, tell the user
            if (data.length === 0)
            {
                $('.results-container').text('No results');
                return;
            }   
            
            // Place each ingredient in the results list.
            for (var idx=0; idx < data.length; idx++)
            {
                ingredient = data[idx];

                content = $('<a>', {
                    href: ingredient.detail_url,
                    text: ingredient.name,
                });

                div = $('<div>', {class: "ingredient-result", html: content});
                $('.results-container').append(div);
            }
        },
    });
};

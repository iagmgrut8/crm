// search.js
$(document).ready(function() {
    $('#search-form').on('submit', function(e) {
        e.preventDefault();  // Prevent form submission

        const searchQuery = $('[name="q"]').val();

        // Make an AJAX request to the server to fetch filtered records
        $.get('/search/', { q: searchQuery }, function(data) {
            $('#records-table').html(data);  // Update the records table
        });
    });
});

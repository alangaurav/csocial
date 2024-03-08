$(document).ready(function () {
    //Handle New Post Modal
    $('#open-modal').click(function () {
        $('.modal-container').load('/newpost/', function (response, status, xhr) {
            if (status == 'error')
                window.replace('/posts/');
            else {
                $('#modal').show();
                $('.modal').css('display', 'flex');

                $('#newpostform').submit(function (event) {
                    event.preventDefault();
                    $.ajax({
                        url: '/newpost/',
                        type: 'POST',
                        data: $(this).serialize(),
                        success: function (response) {
                            window.location.replace('/posts/')
                        },
                        error: function (xhr, status, error) {
                            console.error(error);
                        }
                    });
                });
            }
        });
    });

    //Handle Modal Close
    $(window).click(function (event) {
        if (event.target.id == 'modal') {
            $('#modal').hide();
            $('.modal-container').empty(); // Hide and remove content
        }
    });

    //Handle individual post click
    $('.post-container').click(function (event) {
        $('.modal-container').load('/singlepost/?post=' + this.id, function (response, status, xhr) {
            if (status == 'Error')
                window.replace('/posts/')
            else {
                $('#modal').show(); // Show the modal once content is loaded
                $('.modal').css('display', 'flex');
            }
        });
    })
});

//Handle close modal button
function closeModal() {
    $('#modal').hide();
    $('.modal-container').empty(); // Hide and remove content   
}
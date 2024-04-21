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
                    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
                    const formData = new FormData($(this)[0]);
                    formData.append('csrfmiddlewaretoken', csrfToken);
                    $.ajax({
                        url: '/newpost/',
                        type: 'POST',
                        contentType: false,
                        processData: false,
                        data: formData,
                        success: function (response) {
                            hidepopup();
                            showpopup(response);
                            if (response.invalid == 'False') {
                                setTimeout(function () {
                                    window.location.replace('/posts/');
                                }, 2000);
                            }
                        },
                        error: function (xhr, status, error) {

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
            $('.modal-container').empty();
            location.reload();
        }
    });

    $('.post-container-author, .post-container-tags').on('click', function(event) {
        event.stopPropagation();
    })

    //Handle individual post click
    $('.post-container').on('click', function (event) {
        let postid = this.id;
        $('.modal-container').load('/singlepost/?post=' + postid, function (response, status, xhr) {
            if (status == 'Error')
                window.replace('/posts/')
            else {
                $('#modal').show();
                $('.modal').css('display', 'flex');
            }

            $('#comment-form').submit(function (event) {
                event.preventDefault();
                $.ajax({
                    url: '/newcomment/?post=' + postid,
                    type: 'POST',
                    data: $(this).serialize(),
                    success: function (response) {
                        hidepopup();
                        showpopup(response);
                        setTimeout(function () {
                            window.location.reload();
                        }, 2000);
                    },
                    error: function (xhr, status, error) {
                    }
                });
            })
        });
    });

    $('#searchform').submit(function (event) {
        $.ajax({
            url: '/posts/',
            type: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                $('span.popup-content').text("Search Success!");
                $('.popup-container').show();
                $('.popup-container').css('display', 'flex');
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });

    $('#loginform').submit(function (event) {
        console.log("Login form called");
        event.preventDefault();
        $.ajax({
            url: '/login/',
            type: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                $('.popup-container').css('display', 'none');
                $('.popup-container-content').empty();
                if (response.invalid == 'True') {
                    $('span.popup-container-content').text(response.message);
                    $('.popup-container').show();
                    $('.popup-container').css('display', 'flex');
                    $('.popup-container-content').addClass('popup-container-content-error');
                }
                else
                    window.location.replace('/posts/');
            },
            error: function (xhr, status, error) {

            }
        });
    });

    $('#signupform').submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: '/signup/',
            type: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                hidepopup()
                if (response.invalid == 'True') {
                    $('span.popup-container-content').text(response.message);
                    $('.popup-container').show();
                    $('.popup-container').css('display', 'flex');
                    $('.popup-container-content').addClass('popup-container-content-error');
                }
                else
                    window.location.replace('/login/');
            },
            error: function (xhr, status, error) {

            }
        });
    });

    $('.post-container-delete').click(function (event) {
        console.log(this.id);
        event.preventDefault();
        $.ajax({
            url: '/delete/?post=' + this.id,
            type: 'GET',
            success: function (response) {
                hidepopup();
                showpopup(response);
                setTimeout(function () {
                    window.location.reload();
                }, 2000);
            },
            error: function (xhr, status, error) {

            }
        });
    });
});

function showpopup(response) {
    if (response.invalid == 'True') {
        $('span.popup-container-content').text(response.message);
        $('.popup-container').show();
        $('.popup-container').css('display', 'flex');
        $('.popup-container-content').addClass('popup-container-content-error');
    }
    else if (response.invalid == 'False') {
        $('span.popup-container-content').text(response.message);
        $('.popup-container').show();
        $('.popup-container').css('display', 'flex');
    }
}

function hidepopup() {
    $('.popup-container').css('display', 'none');
    $('.popup-container-content').empty();
}
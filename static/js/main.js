// Main JavaScript - Navigation and Common Features

$(document).ready(function() {
    // Mobile Navigation Toggle
    $('.nav-toggle').click(function() {
        $('.nav-menu').slideToggle();
    });

    // Smooth Scrolling
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 80
            }, 800);
        }
    });

    // Add active class to current nav item
    const currentPage = window.location.pathname;
    $('.nav-menu a').each(function() {
        if ($(this).attr('href') === currentPage) {
            $(this).addClass('active');
        }
    });
});

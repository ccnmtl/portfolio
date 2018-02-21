(function() {
    jQuery(document).ready(function() {
        /* Social-media sharing */
        jQuery('.share-window').click(function(event) {
            var width  = 575,
                height = 400,
                left   = (jQuery(window).width()  - width)  / 2,
                top    = (jQuery(window).height() - height) / 2,
                url    = this.href,
                opts   = 'status=1' +
                ',width='  + width  +
                ',height=' + height +
                ',top='    + top    +
                ',left='   + left;
            window.open(url, 'sharearticle', opts);
            return false;
        });
    });
})();

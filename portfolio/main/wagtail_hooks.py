from django.utils.html import format_html
from wagtail import hooks


@hooks.register('insert_editor_js')
def enable_source():
    return format_html(
        """
        <script>
            registerHalloPlugin('hallohtml');
        </script>
        """
    )

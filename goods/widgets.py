from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html


class CustomAdminFileWidget(AdminFileWidget):
  def render(self, name, value, attrs=None, renderer=None):
    result = []
    if hasattr(value, "url"):
      result.append(
        f'''<a href="{value.url}" target="_blank">
              <img 
                src="{value.url}" alt="{value}" 
                width="200" height="150"
                style="object-fit: cover;"
              />
            </a>'''
      )
    result.append(super().render(name, value, attrs, renderer))
    return format_html("".join(result))

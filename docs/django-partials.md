Django template partials and HTMX can be used together to create dynamic and interactive web applications with minimal JavaScript. Django's templating engine allows for clean HTML generation, and HTMX allows for updating parts of a page without full reloads. Template partials are reusable sections of templates that can be rendered independently.

Usage

- **Separate Partial Templates**:
    
    Create separate template files for the partials you want to update with HTMX.
    
- **Include Partials**:
    
    Use the `{% include 'partial.html' %}` tag in your main template to include the partials.
    
- **HTMX Attributes**:
    
    Add HTMX attributes like `hx-get`, `hx-post`, and `hx-target` to elements that will trigger updates.
    
- **Views**:
    
    Create Django views that render only the partial template when an HTMX request is received.
    
- **django-template-partials**:
    
    Consider using the `django-template-partials` library for more advanced partial rendering. It allows you to define partials within a template and render them individually.
    

Example

Template (my_template.html)

Code

```
<div>  <h1>Main Content</h1>  <div id="content-to-update">    {% include 'my_partial.html' %}  </div>  <button hx-get="/update_partial/" hx-target="#content-to-update">    Update Content  </button></div>
```

Partial Template (my_partial.html)

Code

```
<p>This is the initial content.</p>
```

View (views.py)

Python

```
from django.shortcuts import renderfrom django.http import HttpResponsedef my_view(request):    return render(request, 'my_template.html')def update_partial(request):    return render(request, 'my_partial.html', {'new_content': 'This is the updated content.'})
```

Updated Partial Template (my_partial.html)

Code

```
<p>{{ new_content }}</p>
```

In this example, when the button is clicked, HTMX sends a GET request to the `update_partial` view. The view renders the `my_partial.html` template with the updated content and returns it. HTMX then replaces the content of the `content-to-update` div with the new content.

django-template-partials Example

Template with Partial (my_template.html)

Code

```
{% load partial %}<div>  <h1>Main Content</h1>  <div id="content-to-update">    {% partial name="my_partial" %}      <p>This is the initial content.</p>    {% endpartial %}  </div>  <button hx-get="/update_partial/" hx-target="#content-to-update">    Update Content  </button></div>
```

View (views.py)

Python

```
from django.shortcuts import renderfrom django.http import HttpResponsefrom django_template_partials import render_partialdef my_view(request):    return render(request, 'my_template.html')def update_partial(request):    return render_partial(request, 'my_template.html', 'my_partial', {'new_content': 'This is the updated content.'})
```

In this case, the `django-template-partials` library is used to define and render the partial. The `render_partial` function renders only the specified partial, making it more efficient for updates.
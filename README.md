# django-render-to-pdf
A guide to using `HTML` template to create a `PDF` and `download` without opening the PDF

### Setup
```shell script
git clone https://github.com/ChanduArepalli/django-render-to-pdf.git
cd django-render-to-pdf
pip install -r requirements.txt 
python manage.py runserver
```

<hr>

     
`or`
     

<hr>

### Installation
#### Packages

```shell script
pip install django
pip install --pre xhtml2pdf
```



#### Files

In main project folder `settings.py` file add `template folder` 
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

`utils.py` file in `App` folder
```python
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

```

`views.py` file in `App` folder
```python
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from datetime import datetime
from .utils import render_to_pdf


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            'today': datetime.now(),
            'amount': 1999,
            'customer_name': 'Chandu Arepalli',
            'order_id': 1234567890,
        }
        pdf = render_to_pdf('pdf/invoice.html', data)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("Not found")


class GenerateAndDownloadPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf/invoice.html')
        context = {
            'today': datetime.now(),
            'amount': 1999,
            'customer_name': 'Chandu Arepalli',
            'order_id': 1234567890,
        }
        pdf = render_to_pdf('pdf/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice.pdf"
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
```

`url.py` file in `App` folder
```python
from django.urls import path
from .views import GeneratePdf, GenerateAndDownloadPDF
urlpatterns = [
    path('', GeneratePdf.as_view()),
    path('pdf/', GenerateAndDownloadPDF.as_view()),
]
```

#### Urls
- `Generate PDF` from `GeneratePdf` view [http://127.0.0.1:8000](http://127.0.0.1:8000)
- `Generate PDF` from `GenerateAndDownloadPDF` view [http://127.0.0.1:8000/pdf](http://127.0.0.1:8000/pdf)
- `Download PDF` from `GenerateAndDownloadPDF` view [http://127.0.0.1:8000/pdf?download=1](http://127.0.0.1:8000/pdf?download=1)

##### Notice

You can add advance stuff of `CSS` and python for passing `Objects` to the `HTML`

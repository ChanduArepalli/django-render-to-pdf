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
        # html = template.render(context)
        pdf = render_to_pdf('pdf/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice.pdf"
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
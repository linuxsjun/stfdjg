from web.models import asset_category
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import preppy
import trml2pdf

#函数
def partt(id):
    tid = asset_category.objects.filter(id=id).first()
    if tid.parentid:
        disname = partt(tid.parentid.id) + '/' +  tid.name
        return disname
    else:
        return tid.name

def tt():
    # print(request.scheme)
    # print(request.body)
    # print(request.path)
    # print(request.path_info)
    # print(request.method)
    # print(request.content_type)
    # print(request.content_params)
    # print(request.COOKIES)
    # print(request.FILES)
    # print(type(request.POST))

    # print(request.GET)
    # print(request.POST)
    # print(request.META)
    # print(
    # print(request.path)

    # http://127.0.0.1:8069/web#view_type=kanban&model=product.template&menu_id=305&action=435

    # https://www.qqxiuzi.cn/zh/pinyin/

    # ps = hr_department.objects.all().values_list('name').annotate(num=Count('employee_department__employeeid__asset_property__sid'),picre=Sum('employee_department__employeeid__asset_property__price')).order_by('-picre')
    # ps = hr_department.objects.all().values_list('name').annotate(num=Count('employee_department__employeeid__id'))

    # print("%s\n%s" % (request.method,request.GET))
    pass

def some_view_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    print('pdf')
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

def pdf_rml(request):
    rml_context = dict(
        name='RML Test'
    )

    template = preppy.getModule('hello.rml')
    rml = template.getOutput(rml_context)
    e = trml2pdf.parseString(rml)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="hello.pdf"'

    response.write(e)
    return response
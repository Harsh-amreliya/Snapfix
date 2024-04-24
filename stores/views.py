import os
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from . import forms, models
import pandas as pd
from .models import storedata
from .utils import convert_amount_to_words
from servicestore.views import addservicestore
from client.models import productrequest

def login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)

        if user is not None:

            if user.is_store_owner:
                auth.login(request,user)
                return redirect(addstore)
            elif user.is_service_store_owner:
                auth.login(request,user)
                return redirect(addservicestore)
            else:
                return render(request,'st/login.html',{'msg':'No Role defined'})
        else:
            return render(request,'st/login.html',{'msg':'Invalid Credentials !!'})
    return render(request,'st/login.html')


def index(request):
    user=request.user
    name=user.username
    store = storedata.objects.get(user=request.user)
    isactive = store.is_activee
    products = models.productlisting.objects.filter(user=request.user).filter(active=True).count()

    orderdata = productrequest.objects.all()
    order = {}
    pending={}
    for index in orderdata:
        product_id_dict = eval(index.productid)
        for key in product_id_dict:
            pid = models.productlisting.objects.get(id=key)
            if pid.user.id == request.user.id:
                if index not in order:
                    order[index] = []  # Initialize the list if it doesn't exist
                order[index].append(pid)
                if index.completed== False:
                    if index not in pending:
                        pending[index]=[]
                    pending[index].append(pid)
    ordercount=len(order)
    pendingorders=len(pending)

    return render(request,'st/index.html',{'name':name,'isactive':isactive,'products':products,'order':ordercount,'pendingorders':pendingorders})

def addstore(request):
    entereddetails=storedata.objects.filter(user=request.user).exists()
    if entereddetails:
        return redirect(index)
    else:
        form = forms.addstoreform(request.POST, request.FILES)
        if request.method == 'POST':

            if form.is_valid():
                store = form.save(commit=False)
                store.entered_store_details = True
                store.user = request.user
                store.save()
                return redirect(index)
            else:
                return render(request, 'st/addstore.html', {'msg': 'Invalid Input'})

        return render(request, 'st/addstore.html')


def completed(request,orderid):
    data=productrequest.objects.get(id=orderid)
    data.completed=True
    data.save()
    return redirect(invoice,request.user.id)

def managemystore(request):

    data=models.storedata.objects.get(user=request.user)
    instance=storedata.objects.get(user=request.user.id)
    licd = os.path.basename(instance.storelicencedocument.name)
    ownrd = os.path.basename(instance.ownersdocument.name)
    stimg = os.path.basename(instance.imageofstore.name)

    return render(request,'st/managemystore.html',{'data':data,'licdoc':licd,'owndoc':ownrd,'stimg':stimg})


def updatestore(request,id):
    data=models.storedata.objects.get(id=id)
    form=forms.addstoreform(request.POST,request.FILES,instance=data)
    if request.method=='POST':
        is_activee = int(request.POST.get('is_activee',0))
        if form.is_valid():
            store=form.save(commit=False)
            store.is_activee=is_activee
            store.entered_store_details=True
            store.save()
            return redirect(managemystore)
        else:
            return render(request,'st/managemystore.html',{'msg':'Invalid Input!!!','data':data})
    return render(request,'st/managemystore.html',{'data':data})

def addservice(request):
    return render(request,'st/addservice.html')

def productlisting(request):
    form=forms.addproduct(request.POST,request.FILES)
    storedata=models.storedata.objects.get(user=request.user)
    usemodel=models.usecategory.objects.filter(user=request.user).filter(active=True)
    if request.method=='POST':

        if form.is_valid():
            product=form.save(commit=False)
            product.user=request.user
            product.store=storedata
            product.save()
            return render(request,'st/productlisting.html',{'msg':'Successful !!','data':usemodel})
        else:
            print(form.errors)

            return render(request,'st/productlisting.html',{'msg':'Invalid Input !!','data':usemodel})

    return render(request,'st/productlisting.html',{'data':usemodel})

def usecategorylisting(request):
    form=forms.addusecategory(request.POST)
    if request.method=='POST':
        if form.is_valid():
            ucategory=form.save(commit=False)
            ucategory.user=request.user
            ucategory.save()
            return render(request,'st/usecategorylisting.html',{'msg':'Successfull !!'})
        else:
            return render(request,'st/usecategorylisting.html',{'msg':'Invalid Input !!'})

    return render(request,'st/usecategorylisting.html')

def excelusecategorylisting(request):
    message="Upload your Excel file here. "
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
            df = pd.read_excel(excel_file)

            # Check for missing columns
            expected_columns = ['companyname', 'modelname', 'modelyear']
            missing_columns = [column for column in expected_columns if column not in df.columns]
            if missing_columns:
                message = f"The following columns are missing: {', '.join(missing_columns)}"
            else:
                # Check for empty fields
                empty_fields = []
                for index, row in df.iterrows():
                    for column in df.columns:
                        if column != 'active' and pd.isna(row[column]):
                            empty_fields.append(f"{column} in row {index + 2}")  # Adjust index to 1-based
                if empty_fields:
                    message = f"The following fields are empty: {', '.join(empty_fields)}"
                else:
                    for index, row in df.iterrows():
                        models.usecategory.objects.create(
                            user=request.user,
                            companyname=row['companyname'],
                            modelname=row['modelname'],
                            modelyear=row['modelyear'],
                            active=True

                        )
                    message = 'Data uploaded successfully!'
        else:
            message = 'Only Excel files are allowed.'

    return render(request, 'st/excelusecategory.html', {'msg': message})


def excel_product_upload(request):
    message = "Upload your Excel file here. "
    store_data = storedata.objects.get(user=request.user)
    invalid_ids = []  # List to store invalid usecategorylist IDs and their corresponding row numbers

    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
            df = pd.read_excel(excel_file)

            # Check for missing columns
            expected_columns = ['productname', 'productprice', 'usecategorylist', 'productimage']
            missing_columns = [column for column in expected_columns if column not in df.columns]
            if missing_columns:
                missing_columns_str = ', '.join(missing_columns)
                message = f"The following columns are missing: {missing_columns_str}"
            elif df.isnull().values.any():  # Check for any missing values
                message = "Excel file contains missing values. Please ensure all fields are filled."
            else:
                for index, row in df.iterrows():
                    # Fetch usecategorylist based on provided ID
                    usecategory_id = row['usecategorylist']
                    usecategory_instance = models.usecategory.objects.filter(id=usecategory_id).first()
                    if usecategory_instance:
                        companyname = usecategory_instance.companyname
                        modelyear = usecategory_instance.modelyear

                        # Concatenate the path before product name
                        productimage_path = f"storedata/product_image/{row['productimage'].replace(' ', '_')}"

                        # Create Product object with all fields including productimage
                        product = models.productlisting.objects.create(
                            user=request.user,
                            productname=row['productname'],
                            productprice=row['productprice'],
                            companyname=companyname,
                            modelyear=modelyear,
                            active=True,
                            store=store_data,
                            usecategorylist=usecategory_instance,
                            productimage=productimage_path
                        )
                    else:
                        invalid_ids.append({'id': usecategory_id, 'row': index + 2})  # Save invalid ID and row number
                        # Adjust index to 1-based and add 2 for header row and zero-based index

                if invalid_ids:
                    message = "The following usecategorylist IDs are invalid or not found in the database: "
                    for invalid_id in invalid_ids:
                        message += f"ID: {invalid_id['id']}, Row: {invalid_id['row']}"
                else:
                    message = 'Data uploaded successfully!'
        else:
            message = 'Only Excel files are allowed.'
    return render(request, 'st/excelproduct.html', {'msg': message})

# def useincategorylisting(request):
#     form=forms.adduseincategory(request.POST)
#     if request.method=='POST':
#         if form.is_valid():
#             uincategory=form.save(commit=False)
#             uincategory.user=request.user
#             uincategory.save()
#             return render(request,'st/useincategorylisting.html',{'msg':'Successfull !!'})
#         else:
#             return render(request,'st/useincategorylisting.html',{'msg':'Invalid Input !!'})
#
#     return render(request,'st/useincategorylisting.html')

def manageusecategory(request):
    data=models.usecategory.objects.filter(user=request.user).filter(active=True)
    return render(request,'st/manageusecategory.html',{'data':data})

def deleteusecategory(request,id):
    data=models.usecategory.objects.get(id=id)
    data.active=False
    data.save()
    return redirect(manageusecategory)

def editusecategory(request,id):
    data=models.usecategory.objects.get(id=id)
    return render(request,'st/editusecategory.html',{'data':data})

def updateusecategory(request,id):
    data=models.usecategory.objects.get(id=id)
    form=forms.addusecategory(request.POST,instance=data)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect(manageusecategory)
        else:
            return render(request,'st/editusecategory.html',{'msg':'Invalid Input'})
    return render(request,'st/manageusecategory.html',{'data':data})


# def manageuseincategory(request):
#     data=models.useincategory.objects.filter(user=request.user)
#     return render(request,'st/manageuseincategory.html',{'data':data})
#
# def edituseincategory(request,id):
#     data=models.useincategory.objects.get(id=id)
#     return render(request,'st/edituseincategory.html',{'data':data})
#
# def updateuseincategory(request,id):
#     data=models.useincategory.objects.get(id=id)
#     form=forms.adduseincategory(request.POST,request.FILES,instance=data)
#     if request.method=='POST':
#         if form.is_valid():
#             form.save()
#             return redirect(manageuseincategory)
#         else:
#             return render(request,'st/edituseincategory.html',{'msg':'Invalid Input !!!'})
#     return render(request,'st/manageuseincategory.html',{'data':data})
#
# def deleteuseincategory(request,id):
#     data=models.useincategory.objects.filter(id=id)
#     data.delete()
#     return redirect(manageuseincategory)

def manageproductlisting(request):
    data=models.productlisting.objects.filter(user=request.user).filter(active=True)
    return render(request,'st/manageproductlisting.html',{'data':data})

def editproduct(request,id):
    data=models.productlisting.objects.get(id=id)
    usemodel = models.usecategory.objects.filter(user=request.user).filter(active=True)
    return render(request,'st/editproduct.html',{'data':data,'cardata':usemodel})

def updateproduct(request,id):
    data=models.productlisting.objects.get(id=id)
    form=forms.addproduct(request.POST,request.FILES,instance=data)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect(manageproductlisting)
        else:
            return render(request,'st/editproduct.html',{'msg':'Invalid Input!!'})
    return render(request,'st/manageproduct.html',{'data':data})

def deleteproduct(request,id):
    data=models.productlisting.objects.get(id=id)
    data.active=False
    data.save()
    return redirect(manageproductlisting)

def invoice(request,id):
    orderdata = productrequest.objects.all()
    order = {}

    for index in orderdata:
        product_id_dict = eval(index.productid)
        for key in product_id_dict:
            pid = models.productlisting.objects.get(id=key)
            if pid.user.id == id:
                if index not in order:
                    order[index] = []  # Initialize the list if it doesn't exist
                order[index].append(pid)

    return render(request,'st/invoice.html',{'orderdata':order})

def viewinvoice(request,orderid,id):
    orderdata = productrequest.objects.get(id=orderid)
    order = []
    amount=0
    product_id_dict = eval(orderdata.productid)

    for key in product_id_dict:
        pid = models.productlisting.objects.get(id=key)
        pid.quantity=product_id_dict[key]
        amount += pid.productprice*pid.quantity
        order.append(pid)

    storedetails=storedata.objects.get(user=id)
    gst=(amount*18)/100
    amtwithgst=amount+gst
    words = convert_amount_to_words(int(amtwithgst))

    return render(request, 'st/viewinvoice.html', {'words': words,'amount':amount,'gst':gst,'amtwithgst':amtwithgst,'order':order,'storedetails':storedetails,'orderdata':orderdata})

def logout(request):
    auth.logout(request)
    return redirect(login)


def whatsapp_share(request):
    # Recipient's phone number (with country code) and message
    recipient_number = '9429276624'
    message = 'Check out this awesome link!'

    # Format the WhatsApp share link
    whatsapp_link = f'https://wa.me/{recipient_number}?text={message}'

    # Pass the WhatsApp link in the context
    context = {
        'whatsapp_link': whatsapp_link,
    }

    id=request.user.id
    # Render a template and pass the context
    return redirect(invoice, id)

# def generate_pdf(request):
#     template_path = 'st/viewinvoice.html'
#     context = {'msg': ' ', 'words': ' '}
#
#     # Render HTML template
#     html_string = render_to_string(template_path, context)
#
#     # Create a PDF using weasyprint
#     pdf_data = HTML(string=html_string).write_pdf()
#
#     # Prepare the HTTP response
#     response = HttpResponse(pdf_data, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="your_invoice.pdf"'
#
#     return response
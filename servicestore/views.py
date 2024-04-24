import os
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from . import models
from . import forms
from .utils import convert_amount_to_words
from .models import servicestoredata
from client.models import towingrequest
from servicestore.models import servicelisting
import pandas as pd



# Create your views here.

def servicestoreindex(request):
    user = request.user
    name = user.username
    store=servicestoredata.objects.get(user=request.user)
    isactive=store.is_activee
    services=models.servicelisting.objects.filter(user=request.user).filter(active=True).count()
    store=servicestoredata.objects.get(user=request.user)
    storeid=store.id
    towingrequests=towingrequest.objects.filter(storeid=storeid).filter(completed=False).count()
    clients=towingrequest.objects.filter(storeid=storeid).filter(completed=True).count()
    return render(request,'serv/index.html',{'name':name,'isactive':isactive,'services':services,'towingrequests':towingrequests,'clients':clients})


def addservicestore(request):
    entereddetails = servicestoredata.objects.filter(user=request.user).exists()
    if entereddetails:
        return redirect(servicestoreindex)
    else:
        form = forms.addservicestoreform(request.POST, request.FILES)

        if request.method == 'POST':
            if form.is_valid():
                service = form.save(commit=False)
                service.entered_store_details = True
                service.user = request.user
                service.save()
                return redirect(servicestoreindex)
            else:
                return render(request, 'serv/addservicestore.html', {'msg': 'Invalid Input'})
        return render(request, 'serv/addservicestore.html')



def managemystore(request):

    data=models.servicestoredata.objects.get(user=request.user)
    instance=servicestoredata.objects.get(user=request.user.id)
    licd = os.path.basename(instance.storelicencedocument.name)
    ownrd = os.path.basename(instance.ownersdocument.name)
    stimg = os.path.basename(instance.imageofstore.name)

    return render(request,'serv/managemyservicestore.html',{'data':data,'licdoc':licd,'owndoc':ownrd,'stimg':stimg})

def updateservicestore(request,id):
    data=models.servicestoredata.objects.get(id=id)
    form=forms.addservicestoreform(request.POST,request.FILES,instance=data)
    if request.method=='POST':
        is_activee = int(request.POST.get('is_activee',0))
        if form.is_valid():
            service=form.save(commit=False)
            service.is_activee=is_activee
            service.entered_store_details=True
            service.save()
            return redirect(managemystore)
        else:
            return render(request,'serv/managemyservicestore.html',{'msg':'Invalid Input!!!'})
    return render(request,'serv/managemyservicestore.html',{'data':data})

def servicelisting(request):
    storedetails=servicestoredata.objects.get(user=request.user)
    form=forms.addservice(request.POST,request.FILES)
    if request.method=='POST':
         if form.is_valid():
             service=form.save(commit=False)
             service.user=request.user
             service.store=storedetails
             service.save()
             return render(request,'serv/servicelisting.html',{'msg':'Successful !!!'})
         else:
             return render(request,'serv/servicelisting.html',{'msg':'Invalid input !!!'})

    return render(request, 'serv/servicelisting.html')

def upload_excel(request):
    storedetails = models.servicestoredata.objects.get(user=request.user)

    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        extension = excel_file.name.split('.')[-1].lower()
        if extension not in ['xlsx', 'xls']:
            return render(request, 'serv/serviceexcel.html', {
                'msg': 'Invalid file format. Please upload a valid Excel file with .xlsx or .xls extension.'})
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return render(request, 'serv/serviceexcel.html',
                          {'msg': 'Error reading Excel file: {}'.format(str(e))})

        # Define expected column names
        expected_columns = ['servicename', 'serviceprice', 'towable', 'avgtime', 'serviceimage']

        # Check if all expected columns are present in the DataFrame
        if not set(expected_columns).issubset(df.columns):
            missing_columns = set(expected_columns) - set(df.columns)
            return render(request, 'serv/serviceexcel.html',
                          {'msg': f'Some columns are missing in the Excel file: {", ".join(missing_columns)}'})

        for index, row in df.iterrows():
            product_name = row['servicename']
            product_price = row['serviceprice']
            checkbox_value = row['towable']
            avg_time = row['avgtime']
            image_file = row['serviceimage']
            if pd.isna(product_name) or pd.isna(product_price) or pd.isna(checkbox_value) or pd.isna(
                    avg_time) or pd.isna(image_file):
                return render(request, 'serv/serviceexcel.html',
                              {'msg': 'Some fields are missing in the Excel file. Please check your file.'})

            # Replace white spaces with underscores in image file name
            image_file = image_file.replace(" ", "_")

            # Save the product data to your database
            models.servicelisting.objects.create(
                servicename=product_name,
                serviceprice=product_price,
                towable=checkbox_value,
                serviceimage=f"servicestoredata/service_image/{image_file}",
                active=True,
                store=storedetails,
                user=request.user,
                avgtime=avg_time
            )

        return render(request, 'serv/serviceexcel.html', {'msg': 'Services Listed Successfully '})

    return render(request, 'serv/serviceexcel.html', {'msg': 'Upload your Excel file here.'})
def manageservice(request):
    data=models.servicelisting.objects.filter(user=request.user).filter(active=True)
    return render(request,'serv/manageservice.html',{'data':data})
def editservice(request,id):
    data=models.servicelisting.objects.get(id=id)
    return render(request,'serv/editservice.html',{'data':data})

def updateservice(request,id):
    data=models.servicelisting.objects.get(id=id)
    form=forms.addservice(request.POST,request.FILES,instance=data)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect(manageservice)
        else:
            return render(request,'serv/editservice.html',{'msg':'Invalid input !!!'})
    return render(request,'serv/editservice.html',{'data':data})

def deleteservice(request,id):
    data=models.servicelisting.objects.get(id=id)
    data.active=False
    data.save()
    return redirect(manageservice)

def orders(request,id):
    store_id=servicestoredata.objects.filter(user=id).values('id')
    storeid=0
    for s in store_id:
        storeid=s['id']

    orders=towingrequest.objects.filter(storeid=storeid).filter(istowable=True)
    print(orders)
    servicedata={}
    totalprice=0
    for a in orders:
        templist=[]
        templist.clear()
        servid=a.serviceid.split('-')
        servid.pop()

        for s in servid:
            try:
                service=models.servicelisting.objects.get(id=s)
                templist.append(service)
            except:

                print('except block')
        servicedata[a.id]=templist
        print(servicedata)
    combineddata=orders
    return render(request,'serv/order.html',{'combinedata':combineddata,'servicedata':servicedata})

def serviceorder(request,id):
    store_id = servicestoredata.objects.filter(user=id).values('id')
    storeid = 0
    for s in store_id:
        storeid = s['id']

    orders = towingrequest.objects.filter(storeid=storeid).filter(istowable=False)

    servicedata = {}
    totalprice = 0
    for a in orders:
        templist = []
        templist.clear()
        servid = a.serviceid.split('-')
        servid.pop()

        for si in servid:
            try:
                service = models.servicelisting.objects.get(id=si)
                templist.append(service)
            except:
                print('except block')

        servicedata[a.id] = templist
    combineddata = orders
    return render(request, 'serv/serviceorder.html', {'combinedata': combineddata, 'servicedata': servicedata})

def invoice(request,orderid):
    id=request.user.id
    try:
        orderdata=towingrequest.objects.get(id=orderid)

        serviceidlist=orderdata.serviceid.split('-')
        serviceidlist.pop()
        servicedata=[]
        amount=0
        towing=0
        for i in serviceidlist:
            s=models.servicelisting.objects.get(id=i)
            amount+=s.serviceprice
            if s.towable:
                towing=1
            servicedata.append(s)
        totlamount=0
        if towing:
            totlamount=amount+300
            gst = ((amount+300) * 18) / 100
            amtwithgst = totlamount + gst
        else:
            gst = (amount * 18) / 100
            amtwithgst = amount + gst
        word = convert_amount_to_words(int(amtwithgst))
        print(id)
        storedetails=models.servicestoredata.objects.get(user=id)
    except:
        print("store Has been deleted")
        orderdata=[]
        servicedata=[]
        amount=0
        word=0
        towing=0
        gst=0
        amtwithgst=0
        totlamount=0
        storedetails=0
    return render(request,'serv/serviceinvoice.html',{'orderdata':orderdata,'servicedata':servicedata,'amount':amount,'words':word,'towing':towing,'amount':amount,'gst':gst,'amtwithgst':amtwithgst,'totlamount':totlamount,'storedetails':storedetails})

def ordercompleted(request,orderid):

    orderdata=towingrequest.objects.get(id=orderid)
    orderdata.completed=True
    orderdata.save()
    id=request.user.id
    if orderdata.istowable:
        return redirect(orders,id)
    else:
        return redirect(serviceorder,id)





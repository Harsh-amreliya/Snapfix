from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='cl-index'),
    path('cl-about',views.about,name='cl-about'),
    path('cl-service',views.service,name='cl-service'),
    path('cl-contact',views.contact,name='cl-contact'),
    path('cl-nearbystore/',views.nearbystore, name='cl-nearbystore'),
    path('cl-nearbystore_active/<str:storetype>',views.nearbystore_active, name='cl-nearbystore_active'),
    path('cl-login/',views.login, name='cl-login'),
    path('cl-register',views.register, name='cl-register'),
    path('cl-fetchstore/<str:storetype>',views.fetchstore, name='cl-fetchstore'),
    path('cl-requeststorelisting/',views.requeststorelisting, name='cl-requeststorelisting'),
    path('cl-stores/<int:id>',views.stores, name='cl-stores'),
    path('cl-product/<int:id>',views.products, name='cl-product'),
    path('cl-logout/',views.logout, name='cl-logout'),
    path('cl-cart/<int:id><int:storeid>',views.cartdetails, name='cl-cart'),
    path('cl-dynamicproduct/<int:id><str:type>',views.dynamicproductdata, name='cl-dynamicproduct'),
    path('cl-dynamiccartdata/<int:id><int:storeid>',views.dynamiccartdata, name='cl-dynamiccartdata'),
    path('cl-payment/<int:storeid><str:type>',views.payment, name='cl-payment'),
    path('cl-addtocartproduct/<int:id><int:storeid>',views.addtocartproduct, name='cl-addtocartproduct'),
    path('cl-addtocartservice/<int:id><int:storeid>',views.addtocartservice, name='cl-addtocartservice'),
    path('cl-removeservice/<int:id><int:storeid>',views.removeservice, name='cl-removeservice'),
    path('cl-removeproduct/<int:id><int:storeid>',views.removeproduct, name='cl-removeproduct'),
    path('cl-updatequantity/<int:cartid>/<str:type>',views.updatequantity, name='cl-updatequantity'),
    path('cl-towingrequest/<int:storeid><int:istowable>',views.towingorder, name='cl-towingrequest'),
    path('cl-productrequest/',views.productorder, name='cl-productrequest'),
    path('cl-myorders/<int:id>',views.myorders, name='cl-myorders'),
    path('cl-myproductorders/<int:id>',views.productorders, name='cl-myproductorders'),
    path('cl-update_location/', views.update_location, name='cl-update_location'),
    path('cl-confirmed/', views.confirmed, name='cl-confirmed'),
    path('cl-myorderinvoice/<int:orderid>', views.myorderinvoice, name='cl-myorderinvoice'),
    path('client-product-invoice/<int:orderid>', views.product_invoice, name='client-product-invoice'),

]

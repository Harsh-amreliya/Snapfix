
from django.urls import path
from . import views


urlpatterns = [
    path('st-index',views.index,name='st-index'),
    path('st-addstore',views.addstore,name='st-addstore'),
    path('st-addservice',views.addservice,name='st-addservice'),
    path('st-productlisting',views.productlisting,name='st-productlisting'),
    path('st-usecategorylisting',views.usecategorylisting,name='st-usecategorylisting'),
    path('st-exclel-usecategorylisting',views.excelusecategorylisting,name='st-exclel-usecategorylisting'),
    path('st-exclel-product',views.excel_product_upload,name='st-exclel-product'),
    # path('st-useincategorylisting',views.useincategorylisting,name='st-useincategorylisting'),
    path('st-managemystore',views.managemystore,name='st-managemystore'),
    path('st-manageusecategory',views.manageusecategory,name='st-manageusecategory'),
    # path('st-manageuseincategory',views.manageuseincategory,name='st-manageuseincategory'),
    path('st-manageproductlisting',views.manageproductlisting,name='st-manageproductlisting'),
    path('st-editusecategory/<int:id>',views.editusecategory,name='st-editusecategory'),
    path('st-updateusecategory/<int:id>',views.updateusecategory,name='st-updateusecategory'),
    path('st-updatestore/<int:id>',views.updatestore,name='st-updatestore'),
    path('st-completed/<int:orderid>',views.completed,name='st-completed'),
    path('st-deleteusecategory/<int:id>',views.deleteusecategory,name='st-deleteusecategory'),
    # path('st-edituseincategory/<int:id>',views.edituseincategory,name='st-edituseincategory'),
    # path('st-updateuseincategory/<int:id>',views.updateuseincategory,name='st-updateuseincategory'),
    # path('st-deleteuseincategory/<int:id>',views.deleteuseincategory,name='st-deleteuseincategory'),
    path('st-editproduct/<int:id>',views.editproduct,name='st-editproduct'),
    path('st-updateproduct/<int:id>',views.updateproduct,name='st-updateproduct'),
    path('st-deleteproduct/<int:id>',views.deleteproduct,name='st-deleteproduct'),
    path('st-invoice/<int:id>',views.invoice,name='st-invoice'),
    path('st-viewinvoice/<int:orderid><int:id>',views.viewinvoice,name='st-viewinvoice'),
    path('',views.login,name='st-login'),
    path('st-logout',views.logout,name='st-logout'),
    path('st-share',views.whatsapp_share,name='st-share'),
    # path('st-generate-pdf/',views.generate_pdf, name='st-generate_pdf'),

]

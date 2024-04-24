
from django.urls import path
from . import views


urlpatterns = [
    path('serv-index',views.servicestoreindex,name='serv-index'),
    path('serv-addstore',views.addservicestore,name='serv-addstore'),
    path('serv-updateservicestore/<int:id>',views.updateservicestore,name='serv-updateservicestore'),
    path('serv-managemyservicestore',views.managemystore,name='serv-managemyservicestore'),
    path('serv-servicelistiing',views.servicelisting,name='serv-servicelisting'),
    path('serv-uploadexcel',views.upload_excel,name='serv-uploadexcel'),
    path('serv-editservice/<int:id>',views.editservice,name='serv-editservice'),
    path('serv-manageservice',views.manageservice,name='serv-manageservice'),
    path('serv-updateservice/<int:id>',views.updateservice,name='serv-updateservice'),
    path('serv-deleteservice/<int:id>',views.deleteservice,name='serv-deleteservice'),
    path('serv-serviceinvoice/<int:orderid>',views.invoice,name='serv-serviceinvoice'),
    path('serv-order/<int:id>',views.orders,name='serv-order'),
    path('serv-ordercompleted/<int:orderid>',views.ordercompleted,name='serv-ordercompleted'),
    path('servorder/<int:id>',views.serviceorder,name='servorder'),

]

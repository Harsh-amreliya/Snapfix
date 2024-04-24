
from django.urls import path
from . import views

urlpatterns = [
    path('adindex',views.index,name='ad-index'),
    path('addstore/',views.addstore,name='ad-addstore'),
    path('addservice/',views.addservice,name='ad-addservice'),
    path('editstore/<int:id>',views.editstore,name='ad-editstore'),
    path('editservice/<int:id>',views.editservice,name='ad-editservice'),
    path('managestore/',views.managestore,name='ad-managestore'),
    path('manageservicestore/',views.manageservice,name='ad-manageservicestore'),
    path('adupdatestore/<int:id>',views.adupdatestore,name='ad-adupdatestore'),
    path('addnow/<int:id>',views.addnow,name='ad-addnow'),
    path('deletestore/<int:id>',views.deletestore,name='ad-deletestore'),
    path('deleterequest/<int:id>',views.removerequest,name='ad-deleterequest'),
    path('deleteservice/<int:id>',views.deleteservice,name='ad-deleteservice'),
    path('adupdateservice/<int:id>',views.adupdateservice,name='ad-adupdateservice'),
    path('adduser/',views.registerowner,name='ad-registerstoreuser'),
    path('',views.login,name='ad-login'),
    path('adlogout',views.logout,name='ad-logout'),
    path('storerequest',views.storerequest,name='ad-storerequest'),
]

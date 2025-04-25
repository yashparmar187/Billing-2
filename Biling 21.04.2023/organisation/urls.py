
from django.urls import path
# from .views import OrganisationView,LoginView,index,CustomerView,CustomerFormView,delete,edit,update,logout,invoicePage,InvoiceView
from .views import *

urlpatterns = [
    path('signup/',OrganisationView,name = 'signup'),
    path('',LoginView, name='login'),
    
    # Forget Password -----------
    
    path('forgotpass/',forgot_pass,name = 'forgotpass'),
    path('otpcheck/',otpcheck, name = 'otpcheck'),
    path('newpassword/',newpassword, name = 'newpassword'),
    
    # Forget Password -----------
    
    path('index/',index, name = 'index'),
    path('customer/',CustomerView,name = 'customer'),
    path('customerform/',CustomerFormView,name = 'customerform'),
    path('customerDelete/<int:cust_del>/',CustomerDelete,name='CustDel'),
    path('customerUpdate/<int:cust_up>/',CustomerUpdate,name='CustUp'),
    path('invoiceview/',InvoiceView,name = 'invoiceview'),
    path('invoicepage/<int:id>/',InvoicePage,name='invopage'),
    path('invoiceform/',InvoiceForm,name='invoiceform'),
    path('invoiceDelete/<int:invo_del>/',InvoiceDelete,name='InvoDel'),
    path('invoiceUpdate/<int:invo_up>/',InvoiceUpdate,name='InvoUp'),
    path('productview/',ProductView,name = 'productview'),
    path('productform/',ProductForm,name='productform'),
    path('addProductForm/',addProductForm,name='addProductForm'),
    path('updateaddProductForm/<int:id>',updateaddProductForm,name='updateaddProductForm'),
    path('viewquentity/',viewquentity,name='viewquentity'),
    path('productDelete/<int:prod_del>/',ProductDelete,name='ProdDel'),
    path('productUpdate/<int:prod_up>/',ProductUpdate,name='ProdUp'),
    path('detailpage/<int:id>',DetailPage,name='detailpage'),
    path('logout/',logout,name = "logout"),
    path('all_invoices/',Total_Invoice_Page,name='total_invoice_page'),
    
    # HTml To PDF -------------
    path('Generatedpdf/<int:id>',GeneratePdf,name="pdf"),
    
    # QRCode -------------
    path('QRCode_Generate/<int:id>/',QRCode_Generate,name='qrcode'),
    
    # Email --------
    path('SendMail/<int:id>',EmailCall,name='email'),
]
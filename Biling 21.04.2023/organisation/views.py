from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import OrganisationDetails,CustomerDetails,Invoice_Details,Product,AddProduct
from .forms import OrganisationForm,CustomerForm,Invoice_Details_Form,Product_Form
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.contrib import messages

# Forget PAssword -------
import random

# QRCode
import qrcode
from django.conf import settings # new

#email --------- 
import smtplib
import email.message
from smtplib import SMTP 


# Html To Pdf -------------------

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.http import HttpResponse

# Html To Pdf -------------------

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def GeneratePdf(request,id):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        invo = Invoice_Details.objects.get(id=id)
        prod = Product.objects.filter(Invoice=invo)
        cust_data = CustomerDetails.objects.get(cust_name=invo.Cust_name)
        tot = 0
        for i in prod:
            tot += float(i.Total)
        data = {'org':org,'cust':cust_data,'invo':invo,'prod':prod,'tot':tot}
        pdf = render_to_pdf('GeneratePdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('login')

# QRCode -------------------------
def QRCode_Generate(request,id):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        invo = Invoice_Details.objects.get(id=id)
        prod_no = Product.objects.filter(Invoice=invo).count()
        prod = Product.objects.filter(Invoice=invo)
        cust_data = CustomerDetails.objects.get(cust_name=invo.Cust_name)
        tot = 0
        for i in prod:
            tot += float(i.Total)
        # data = {'org':org,'cust':cust_data,'invo':invo,'prod':prod,'tot':tot}
        
        first = f"""
            Company Name : {org.company_name}
            Customer Name : {cust_data.cust_name}
            Invoice No. : {invo.Invoice_num}
            Total Products : {prod_no}
        """
        sec = ""
        for pr in prod:
            sec += """
            Product Name : """ + str(pr.Product_name) + """
            Product Qty : """ + str(pr.Qty) + """
            Product Price : """ + str(pr.Price) + """
            Product Total : """ + str(pr.Total) + "\n"
             
        third = f"""
            Total Amount To Pay : {tot}
        """
        
        data = first + sec + third
        
        qr = qrcode.QRCode(version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                   box_size=10,border=4,)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        qrcode_nm = str(invo.Invoice_num)+".jpg"
        qrcode_path = settings.MEDIA_ROOT+"/"+qrcode_nm
        print(qrcode_path)
        img.save(qrcode_path)
        
        invo.qrcode = qrcode_nm
        invo.save()
        
        return render(request,'View_QRCode.html',{'org':org,'cust':cust_data,'invo':invo,'tot':tot})
        
    else:
        return redirect('login')

# Email ------------------

def EmailCall(request,id):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        invo = Invoice_Details.objects.get(id=id)
        prod = Product.objects.filter(Invoice=invo)
        cust_data = CustomerDetails.objects.get(cust_name=invo.Cust_name)
        tot = 0
        for i in prod:
            tot += float(i.Total)
        data = {'org':org,'cust':cust_data,'invo':invo,'prod':prod,'tot':tot}
        
        
        # my_email = "darpansalunkework@gmail.com"
        # my_pass = "darpan@work"
        # fr_email = "darpansalunke@gmail.com"
        try:
            my_email = org.email
            my_pass = org.password_2
            fr_email = cust_data.email
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            
            mead_data =""
                
            front = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div>
                        <h2>Company Name : """ + org.company_name + """</h2>
                        <h2>Customer Name : """ + cust_data.cust_name + """</h2>
                        <h2>Invoice No. : """ + invo.Invoice_num + """</h2>
                    </div>
                    <br>
                    <div>
                        <table border="2">
                            <thead>
                                <tr>
                                    <th>
                                        Product Name
                                    </th>
                                    <th>
                                        Hsn Code
                                    </th>
                                    <th>
                                        Qty
                                    </th>
                                    <th>
                                        Price
                                    </th>
                                    <th>
                                        Discount
                                    </th>
                                    <th>
                                        Cgst
                                    </th>
                                    <th>
                                        Sgst
                                    </th>
                                    <th>
                                        Igst
                                    </th>
                                    <th>
                                        Cess
                                    </th>
                                    <th>
                                        Total
                                    </th>
                                </tr>
                            </thead>
                            <tbody>"""
                            
            for i in prod:
                mead_data += """<tr>
                <td>""" + str(i.Product_name) + """ </td>
                <td>""" + str(i.Hsn_code) + """ </td> 
                <td>""" + str(i.Qty) + """</td>
                <td>""" + str(i.Price) + """</td>
                <td>""" + str(i.Discount) + """</td>
                <td>""" + str(i.Cgst) + """</td>
                <td>""" + str(i.Sgst) + """</td>
                <td>""" + str(i.Igst) + """</td>
                <td>""" + str(i.Cess) + """</td>
                <td>""" + str(i.Total) + """</td>
                </tr> """
                
            ended = f"""
            </tbody> </table> </body> </html>
            <h2> Amount To Pay : {tot} <h2>"""
            
            email_content = front + mead_data + ended
            print(email_content)
            
            msg = email.message.Message()
            msg['Subject'] = f'Your Invoice No. {invo.Invoice_num} From {org.company_name}' 
            msg['From'] = my_email
            msg['To'] = fr_email
            password = my_pass
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s = smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
        
            # return HttpResponse("<h1>Email Sent<h2>")
            data1 = "Email Sent"
            return render(request,'Error_Show.html',{'data1':data1})
        except:
            data1 = "Email Not Sent"
            data2 = "Maybe Your Email Id Or Password Is Wrong"
            return render(request,'Error_Show.html',{'data1':data1,'data2':data2})
            
    else:
        return redirect('login')

# Organisation -------------

def OrganisationView(request):
    forms = OrganisationForm(request.POST or None)
    if request.POST:
        if forms.is_valid():
            try:
                valid = OrganisationDetails.objects.get(user_id=request.POST['user_id'])
                return HttpResponse("<h2><a href=''>User Id Already In Use </a></h2>")
            except:
                forms.save()
                request.session['org'] = request.POST['user_id']
                return redirect('login')
        else:
            print('not valid')
    else:
        print('not post')
    return render(request,'signup.html',{'org':forms})

def LoginView(request):
    if request.method == "POST":
        try:
            m = OrganisationDetails.objects.get(user_id = request.POST['username'])
            if m.password_2 == request.POST['password']:
                print(m.user_id)
                request.session['org'] = m.user_id
                request.session['orgid'] = m.pk
                return redirect('index')
            else:
                return HttpResponse("<h2><a href=''>You have entered wrong password</a></h2>")
        except:
            return HttpResponse("<h2><a href=''>no username found.</a></h2>")
    return render(request,'registration/login.html')

# Forget Password -----------------

def forgot_pass(request):
    if request.POST:
        email1 = request.POST['email']
        number1 = request.POST['m_no']
            
        try:
            valid = OrganisationDetails.objects.get(email=email1)
            if int(valid.phone) == int(number1):
                print(email1)
                request.session['useremail'] = email1
                
                numbers = [1,2,3,4,5,6,7,8,9,0]
                num = ""
                for i in range(4):
                    num += str(random.choice(numbers))
                
                num = int(num)
                print(num)
                
                # ============== Email ==============
                
                sender_email = "subhashdantani98@gmail.com"
                sender_pass = "picflwwetzovlpuz"
                receiver_email = email1

                server = smtplib.SMTP('smtp.gmail.com',587)

                your_message = "This Is Your OTP Number = "+str(num)

                print(your_message)

                msg = email.message.Message()
                msg['Subject'] = "Your OTP From Advance Billing System"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                password = sender_pass
                msg.add_header('Content-Type','text/html')
                msg.set_payload(your_message)

                server.starttls()
                server.login(msg['From'],password)
                server.sendmail(msg['From'],msg['To'],msg.as_string())
                
                # ============== End Email ===========
                
                request.session['otp'] = num
                
                return render(request,'OTP.html',{'otp':num})
                                    
            else:
                messages.add_message(request, messages.ERROR, "Mobile Number Is Not Registered ")
                return redirect('forgotpass')
        except:
            messages.add_message(request, messages.ERROR, "Email Is Not Registered")
            return redirect('forgotpass')
        
    return render(request,'Forget_Pass.html')

def otpcheck(request):
    if request.session.has_key('otp'):
        if request.POST:
            otp = request.POST['otp']
            if int(request.session['otp']) == int(otp):
                del request.session['otp']
                return redirect('newpassword')
            else:
                return HttpResponse("<h2><a href=""> You Have Entered Wrong OTP </a></h2>")
        else:
            return redirect('forgotpass')
    return redirect('login')

def newpassword(request):
    if request.session.has_key('useremail'):
        if request.POST:
            pass_1 = request.POST['pass1']
            pass_2 = request.POST['pass2']
            
            if pass_1 == pass_2:
                valid = OrganisationDetails.objects.get(email=request.session['useremail'])
                valid.password_1 = pass_2
                valid.password_2 = pass_2
                valid.save()
                del request.session['useremail']
                return redirect('login')
            else:
                messages.add_message(request, messages.ERROR, "Passwords Are Not Same ...")
        return render(request,'New_Pass.html')
    return redirect('login')


def index(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        cust_count = CustomerDetails.objects.all().filter(companyName=org).count()
        cust = CustomerDetails.objects.all().filter(companyName=org)
        tot_invo = 0
        for i in cust:
            invoice_count = Invoice_Details.objects.all().filter(Cust_name=i).count()
            tot_invo += invoice_count
        return render(request,'index.html',{'org':org.company_name,'cust_count':cust_count,'invo_count':tot_invo})
    else:
        return redirect('login')
    
# Customer Data ---------------
   
def CustomerView(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        model = CustomerDetails.objects.all().filter(companyName=org)
        return render(request,'customer.html',{'org':org.company_name,'customerdata':model})
    else:
        return redirect('login')

def CustomerFormView(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        if request.POST:
            cust = CustomerDetails()
            cust.companyName = org
            cust.cust_name = request.POST['cust_name']
            cust.cont_person = request.POST['cont_person']
            cust.contact_num = request.POST['contact_num']
            cust.email = request.POST['email']
            cust.company_type = request.POST['company_type']
            cust.address = request.POST['address']
            cust.address_2 = request.POST['address_2']
            cust.landmark = request.POST['landmark']
            cust.country = request.POST['country']
            cust.state = request.POST['state']
            cust.city = request.POST['city']
            cust.pincode = request.POST['pincode']
            cust.save()
            return redirect('/customer')
        return render(request,'customerform.html',{'org':org.company_name})
    else:
        return redirect('login')

def CustomerDelete(request,cust_del):
    if 'org' in request.session:
        data = CustomerDetails.objects.get(id=cust_del)
        data.delete()
        return redirect('customer')
    else:
        return redirect ('login')
    
def CustomerUpdate(request,cust_up):  
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        cust = CustomerDetails.objects.get(id=cust_up)
        if request.POST:
            cust.companyName = org
            cust.cust_name = request.POST['cust_name']
            cust.cont_person = request.POST['cont_person']
            cust.contact_num = request.POST['contact_num']
            cust.email = request.POST['email']
            cust.company_type = request.POST['company_type']
            cust.address = request.POST['address']
            cust.address_2 = request.POST['address_2']
            cust.landmark = request.POST['landmark']
            cust.country = request.POST['country']
            cust.state = request.POST['state']
            cust.city = request.POST['city']
            cust.pincode = request.POST['pincode']
            cust.save()
            return redirect('customer')
        return render(request,'customerform.html',{'org':org.company_name,'data':cust})
    else:
        return redirect('login')

# Invoice Data ---------------

def Total_Invoice_Page(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        in_data = Invoice_Details.objects.filter(companyName=org)
        invo = []
        pro = []
        pro_tot = []
        for i in in_data:
            print(i)
            invo.append(i)
            pro_count = Product.objects.filter(Invoice=i).count()
            print(pro_count)
            pro.append(pro_count)
            t = 0
            pro_data = Product.objects.filter(Invoice=i)
            for i in pro_data:
                t += float(i.Total)
            pro_tot.append(t)
            
        data = zip(invo,pro,pro_tot)
        return render(request,'Total_Invoice_Page.html',{'org':org.company_name,'invo':data})
    else:
        return redirect('login')

def InvoiceView(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        cust_data = CustomerDetails.objects.all().filter(companyName=org)
        cust = []
        inv = []
        for i in cust_data:
            print(i)
            cust.append(i)
            in_data = Invoice_Details.objects.filter(Cust_name=i).count()
            print(in_data)
            inv.append(in_data)
        
        data = zip(cust,inv)
        return render(request,'temp_invoice.html',{'org':org.company_name,'data':data})
    else:
        return redirect('login')

def InvoicePage(request,id):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        cust_data = CustomerDetails.objects.get(id=id)
        in_data = Invoice_Details.objects.filter(Cust_name=cust_data)
        invo = []
        pro = []
        pro_tot = []
        
        for i in in_data:
            print(i)
            invo.append(i)
            pro_count = Product.objects.filter(Invoice=i).count()
            print(pro_count)
            pro.append(pro_count)
            t = 0
            pro_data = Product.objects.filter(Invoice=i)
            for i in pro_data:
                t += float(i.Total)
            pro_tot.append(t)
            
        data = zip(invo,pro,pro_tot)
        return render(request,'invoice_list.html',{'org':org.company_name,'cust':cust_data,'invo':data})
    else:
        return redirect('login')
    
def DetailPage(request,id):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        invo = Invoice_Details.objects.get(id=id)
        prod = Product.objects.filter(Invoice=invo)
        cust_data = CustomerDetails.objects.get(cust_name=invo.Cust_name)
        tot = 0
        for i in prod:
            tot += float(i.Total)
        return render(request,'DetailPage.html',{'org':org.company_name,'cust':cust_data,'invo':invo,'prod':prod,'tot':tot})
    else:
        return redirect('login')

def InvoiceForm(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        cust_data = CustomerDetails.objects.all().filter(companyName=org)
        invo_prev = Invoice_Details.objects.all().order_by('-id')[0]
        if request.POST:
            invo = Invoice_Details()
            invo.companyName = org
            invo.Cust_name = CustomerDetails.objects.get(cust_name=request.POST['Cust_name'])
            invo.Invoice_type = request.POST['Invoice_type']
            invo.Invoice_num = "Invo"+str(invo_prev.id+1)
            invo.Date = request.POST['Date']
            invo.Dispatch_through = request.POST['Dispatch_through']
            invo.Due_date = request.POST['Due_date']
            invo.Bank = request.POST['Bank']
            invo.Payment_type = request.POST['Payment_type']
            invo.Payment_note = request.POST['Payment_note']
            invo.T_c = request.POST['T_c']
            invo.Document_note = request.POST['Document_note']
            invo.save()
            return redirect('invoiceview')
        return render(request,'invoiceform.html',{'org':org.company_name,'cust':cust_data})
    else:
        return redirect('login')

def InvoiceDelete(request,invo_del):
    if 'org' in request.session:
        data = Invoice_Details.objects.get(id=invo_del)
        data.delete()
        return redirect('invoiceview')
    else:
        return redirect('login')
    
def InvoiceUpdate(request,invo_up):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        cust_data = CustomerDetails.objects.all().filter(companyName=org)
        invo = Invoice_Details.objects.get(id=invo_up)
        if request.POST:
            invo.companyName = org
            invo.Cust_name = CustomerDetails.objects.get(cust_name=request.POST['Cust_name'])
            invo.Invoice_type = request.POST['Invoice_type']
            invo.Invoice_num = request.POST['Invoice_num']
            invo.Date = request.POST['Date']
            invo.Dispatch_through = request.POST['Dispatch_through']
            invo.Due_date = request.POST['Due_date']
            invo.Bank = request.POST['Bank']
            invo.Payment_type = request.POST['Payment_type']
            invo.Payment_note = request.POST['Payment_note']
            invo.T_c = request.POST['T_c']
            invo.Document_note = request.POST['Document_note']
            invo.save()
            return redirect('invoiceview')
        return render(request,'invoiceform.html',{'data':invo,'org':org.company_name,'cust':cust_data})
    else:
        return redirect('login')

# Product Data -------------------

def ProductView(request):
    if 'org' in request.session:
        pro_data = Product.objects.all()
        return render(request,'temp_product.html',{'prod_data':pro_data})
    else:
        return redirect('login')

def ProductForm(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        invo = Invoice_Details.objects.filter(companyName=org)
        prod2=AddProduct.objects.filter(companyName=org)
        if request.POST:
            prod = Product()
            prod.companyName = org
            prod.Invoice = Invoice_Details.objects.get(Invoice_num=request.POST['Invoice'])
            prod.Product_name = request.POST['Product_name']
            prod.Hsn_code = request.POST['Hsn_code']
            prod.Qty = request.POST['Qty']
            prod.Price = request.POST['Price']
            prod.Discount = request.POST['Discount']
            prod.Cgst = request.POST['Cgst']
            prod.Sgst = request.POST['Sgst']
            prod.Igst = request.POST['Igst']
            prod.Cess = request.POST['Cess']
            prod.Total = request.POST['Total']
            a=AddProduct.objects.get(Product_name=request.POST['Product_name'],companyName=org.pk)
            if a.Qty>=int(request.POST['Qty']):
                prod.save()
                a.Qty=a.Qty-int(prod.Qty)
                a.save()
                return redirect('/invoiceview/')
            else:
                return render(request,'productform.html',{'org':org.company_name,'invo':invo,'prod':prod2,"m":"Quantity Not Available" })
        return render(request,'productform.html',{'org':org.company_name,'invo':invo,'prod':prod2})
    else:
        return redirect('login')

def viewquentity(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        data=AddProduct.objects.filter(companyName=request.session['orgid'])
        return render(request,'viewQuntity.html',{'org':org.company_name,'data':data})
    else:
        return redirect('login')
def addProductForm(request):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        if request.POST:
            prod = AddProduct()
            prod.companyName = org
            prod.Product_name = request.POST['Product_name']
            prod.Qty = request.POST['Qty']
            prod.save()
            return redirect('/invoiceview/')
        return render(request,'addproduct.html',{'org':org.company_name})
    else:
        return redirect('login')

def updateaddProductForm(request,id):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        prod = AddProduct.objects.get(id=id)
        if request.POST:
            prod.companyName = org
            prod.Product_name = request.POST['Product_name']
            prod.Qty = request.POST['Qty']
            prod.save()
            return redirect('/viewquentity/')
        return render(request,'updateaddproduct.html',{'org':org.company_name,'prod':prod})
    else:
        return redirect('login')

def ProductDelete(request,prod_del):
    if 'org' in request.session:
        data = Product.objects.get(id=prod_del)
        a=AddProduct.objects.get(Product_name=data.Product_name,companyName=request.session['orgid'])
        a.Qty=float(a.Qty)+float(data.Qty)
        a.save()
        data.delete()
        return redirect('/invoiceview/')
    else:
        return redirect('login')
    
def ProductUpdate(request,prod_up):
    if 'org' in request.session:
        org = OrganisationDetails.objects.get(user_id = request.session['org'])
        invo = Invoice_Details.objects.filter(companyName=org)
        prod = Product.objects.get(id=prod_up)
        a=AddProduct.objects.get(Product_name=prod.Product_name,companyName=request.session['orgid']) 
        xy=prod.Qty
        print("hello",a.Qty,xy)
        if request.POST:
            prod.companyName = org
            prod.Invoice = Invoice_Details.objects.get(Invoice_num=request.POST['Invoice'])
            prod.Product_name = request.POST['Product_name']
            prod.Hsn_code = request.POST['Hsn_code']
            prod.Qty = request.POST['Qty']
            prod.Price = request.POST['Price']
            prod.Discount = request.POST['Discount']
            prod.Cgst = request.POST['Cgst']
            prod.Sgst = request.POST['Sgst']
            prod.Igst = request.POST['Igst']
            prod.Cess = request.POST['Cess']
            prod.Total = request.POST['Total']
            r=float(a.Qty)+float(xy)
            print(a.Product_name,"RRRRRRR",r,"prodqty",prod.Qty)
            if r>=float(request.POST['Qty']):
                if float(xy)==float(request.POST['Qty']):
                    print("son")
                    prod.save()
                    return redirect('/invoiceview/')
                elif float(xy)<float(request.POST['Qty']):
                    newqty=float(request.POST['Qty'])-float(xy)
                    a.Qty=float(a.Qty)-float(newqty)
                    print("father")
                    prod.save()
                    a.save()
                    return redirect('/invoiceview/')
                elif float(xy)>float(request.POST['Qty']):
                    newqty=float(xy)-float(request.POST['Qty'])
                    print("mother")
                    prod.save()
                    a.Qty=float(a.Qty)+float(newqty)
                    a.save()
                    return redirect('/invoiceview/')
            else:
                return render(request,'updateproduct.html',{'org':org.company_name,'invo':invo,'data':prod,"m":"Quantity Not Available" })
        return render(request,'updateproduct.html',{'org':org.company_name,'invo':invo,'data':prod})
    else:
        return redirect('login')

def logout(request):
    if 'org' in request.session:
        del request.session['org']
        return redirect('login')
    else:
        return redirect('login')


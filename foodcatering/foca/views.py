from django.shortcuts import render,redirect
from django.http import HttpResponse
from foca.forms import UserForm,RegForm
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required 
from django.core.mail import send_mail
from foodcatering import settings
from foca.models import Menu,UserData
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from foodcatering import settings

# Create your views here.
def show(request):
  menu=Menu.objects.all()
  return render(request,"frontpg.html",{'menu':menu})

def customreg(request): 
    if request.method=="POST": 
        user=UserForm(request.POST) 
        form=RegForm(request.POST) 
        if user.is_valid() and form.is_valid(): 
            profile = form.save(commit=False) 
            profile.user = request.user 
            user.save() 
            profile.save() 
            return redirect("/login/") 
    else: 
        user=UserForm() 
        form=RegForm() 
    return render(request,"registration/customreg.html",{'form':form,'user':user})

def check(request): 
    username=request.POST['username'] 
    password=request.POST['password'] 
    user=authenticate(request,username=username,password=password) 
    if user is not None: 
        login(request,user)#logs in the user 
        return redirect("/home") 
    else: 
        return redirect("/login") 

@login_required 
def home(request):
    menu=Menu.objects.all()
    username=request.user.username
    i=request.user.id
    request.session['id']=i
    request.session['uname']=username
    return render(request,"home.html",{'menu':menu})  

def logoutview(request): 
    logout(request)#logsout the current user 
    return redirect("/index") 



def buy(request,id,qnt):
  menu=Menu.objects.all()
  item=Menu.objects.get(id=id)
  i=request.session['id']
  customer=UserData.objects.get(user=i)
  st='*'+item.name+"  Rs"+str(item.price)+'   '+str(qnt)+'  Rs'+str(item.price*qnt)
  customer.order=customer.order+st
  customer.tamt=customer.tamt+item.price*qnt
  customer.save()
  return redirect('/home')

def sendmail(request):
    if request.method=="POST":
         subject = "Greetings from Food and Catering"
         msg = "Congratulations your email has been registered with us. We will inform you when we have latest offers"
         to = request.POST['Email']
         res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
         if(res == 1):
              msg = "Mail sent successfully"
         else:
              msg = "Mail could not be sent"
         return HttpResponse(msg)
    else:
        return render(request,'frontpg.html')
def mail(request):
  i=request.session['id']
  customer=UserData.objects.get(user=i)
  order=customer.order
  customer.order=customer.order+"    *----------------------------------------------------------------- * "
  customer.order=customer.order+"    * TOTAL AMOUNT       = Rs"+str(customer.tamt)
  subject="FOOD CATERING SERVICES - BILL"
  msg="";boo=True
  for i in order:
    if(boo and i=='*'):
      msg+="<br>-------------------------------------------------------------------<br><br>"
      boo=False
    if(i=='*'):
      msg+='<br>'
    else:
      msg+=i
  to='akashkbhagat221199@gmail.com'
  res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
  if(res==1):
    msg2=msg
  else:
    msg2="mail could not be sent"
  customer.order=''
  customer.save()
  return HttpResponse(msg2)

def confirm(request):
  i=request.session['id']
  customer=UserData.objects.get(user=i)
  total=customer.tamt
  customer.order=customer.order+"    *----------------------------------------------------------------- * "
  customer.order=customer.order+"    * TOTAL AMOUNT       = Rs"+str(total)
  order=customer.order
  response=HttpResponse(content_type='application/pdf')
  response['Content-Disposition']='attachment;filename="bill.pdf"'
  c=canvas.Canvas(response)
  c.setFont("Times-Roman",20)
  c.drawString(150,700,"FOOD CATERING SERVICE")
  c.drawString(200,650,"BILLING ;-)")
  x=50;y=500;boo=True
  for i in order:
    if(boo and i=='*'):
      y-=30
      x=50
      c.drawString(x,y,"-------------------------------------------------------------------")
      y-=50
      c.setFont("Times-Roman",15)
      boo=False
    if(i=='*'):
      y-=30
      x=50
    else:
      x+=14
      c.drawString(x,y,i)
  c.showPage()
  c.save()
  
  return response



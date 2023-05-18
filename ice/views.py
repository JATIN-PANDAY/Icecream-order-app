from django.shortcuts import render,redirect
from ice.models import *
from django.contrib import messages

# For payment in Instamojo
from django.conf import settings    
from instamojo_wrapper import Instamojo
"import pdb; pdb.set_trace()"

api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN,endpoint="https://test.instamojo.com/api/1.1/")  



def index (request):
    ice=Icecream.objects.all()
    context={
        'ice':ice
    }
    return render(request,'ice.html',context)

def contact (request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        textarea=request.POST['desc']
        var = Contact(Name=name,Email=email,Textarea=textarea)
        var.save()
        messages.success(request, 'Message has been sent')

    return render(request,'cont.html')

def services (request):
    return render(request,'services.html')

def about (request):
    return render(request,'about.html')




def register(request):
    if request.method=="POST":
        name=request.POST['name']
        passw=request.POST['password']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']

        account=UserMaster.objects.filter(email=email)
        
        if account:
            message='User already register'
            return render(request,'register.html',{'msg':message})
        else:
            new=UserMaster.objects.create(email=email,password=passw)
            new_account=User.objects.create(Username=name,user_id=new,Address=address,Mobileno=phone)
            message="Your account created please login to continue"
            return render(request,'login.html',{'msg':message})
    return render(request,'register.html') 



def login(request):
    if request.method=="POST":
        try:
            Email=request.POST['email']
            password=request.POST['password']

            user=UserMaster.objects.get(email=Email)
            
            if user:
                if user.password==password:
                    cand=User.objects.get(user_id=user)
                    request.session['id']=user.id
                    request.session['Name']=cand.Username
                    request.session['Email']=user.email
                    return redirect('/userpage')
                else:
                    message='Please enter correct Password' 
                    return render(request,'login.html',{'msg':message})
        except Exception as e:
            message='Something went wrong'
            return render(request,'login.html',{'msg':message}) 
              
    return render(request,'login.html') 

def logout(request):
    del request.session['Name']
    del request.session['Email']
    return redirect('/')

def userpage(request):
    master=request.session['id']
    user=User.objects.get(user_id=master)

    ice=Icecream.objects.all()
    cart=Cartitems.objects.filter(cart__is_paid=False,cart__user=user).count()

    context={
        'ice':ice ,
        'cart':cart
    }

    return render(request,'home.html',context)



def icecream_name(request,pk):
    master=request.session['id']
    if master:
        user=User.objects.get(user_id=master)
        ice=Icecream.objects.get(id=pk)
        context={'ice':ice,'user':user}
        return render(request,'order.html',context)







def payment_process(request,pk):
    master=request.session['id']
    user=User.objects.get(user_id=master)
    ice=Icecream.objects.get(id=pk)
    order_obj = Order.objects.get_or_create(user_id=user,icecream=ice,price=ice.price,is_paid=False)

    response = api.payment_request_create(
        amount=ice.price,  
        purpose = 'Order',
        buyer_name = user,               
        redirect_url = "http://127.0.0.1:8000/success",
        
    )

    print(response)
    print (response['payment_request']['id'])
    # order_obj.order_id=response['payment_request']['id']
    # order_obj.save()


    context={

        'ice':ice ,
        'payment_url':response['payment_request']['longurl']

            }
            
    return render(request,'pay.html',context)



def success(request):
    master=request.session['id']
    user = User.objects.get(user_id=master)
    # order = Order.objects.get(order=payment_request_id)
    # order=Order.objects.get(pk=id)
    # order.is_paid=True
    # order.save()
    return render(request,'success.html')
    

def userorderpage(request,pk):
    master=request.session['id']
    user=User.objects.get(user_id=master)
    if user:
        var=Order.objects.filter(user_id=user)
        context={
            'var':var
        }
        return render(request,'orderpage.html',context)




def cart(request,pk):
    master=request.session['id']
    user=User.objects.get(user_id=master)
    ice=Icecream.objects.get(id=pk)
    cart , _  = Cart.objects.get_or_create(user=user,is_paid=False)
   
    cart_items=Cartitems.objects.create(cart=cart,icecream=ice)
    return redirect('/userpage')



def showcart(request):
    try:
        master=request.session['id']
        user=User.objects.get(user_id=master)
        cart=Cart.objects.get(user=user,is_paid=False)

        context={
            'user':user,'cart':cart ,
            
                    }
        return render(request,'cart.html',context)
    except Exception as e:
        return render(request,'404.html')


def deleteitems(request,pk):
    master=request.session['id']
    user=User.objects.get(user_id=master)
    cart=Cartitems.objects.get(id=pk)
    cart.delete()
    return redirect('showcart')
















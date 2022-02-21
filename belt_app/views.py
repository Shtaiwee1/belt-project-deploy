from django.shortcuts import render , redirect
from .models import User , Wish
from django.contrib import messages
import bcrypt


def index(request):
        context = {
            'all_users':User.objects.all()
            
        }
        return render(request, 'index.html',context)
    
def process_reg(request):
    errors = User.objects.basic_validator(request.POST)#passes the data from form to the validators function in models which are then called (postData)-validates and then returns errors from the models page
    request.session["coming_from"]="REGISTER"
    if len(errors) > 0:#if there are errors loop through keys and values in the errors dictionary
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['first_name']=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(first_name=request.session['first_name'],
                                        last_name=last_name,
                                        email=email,
                                        password=hashed_password)
        return redirect('/wishes') 
    
def process_login(request):
    errors = User.objects.basic_validator_second(request.POST)
    request.session["coming_from"]="LOGIN"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        find_user=User.objects.filter(email=request.POST['email_login'])
        if find_user:
            logged_user = find_user[0]
            if bcrypt.checkpw(request.POST['password_login'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['first_name'] = logged_user.first_name
                request.session['last_name'] = logged_user.last_name
                request.session['email'] = logged_user.email
                return redirect('/wishes')
        return redirect('/')
    
def wishes(request):
    if "email" not in request.session:
        return redirect('/')
    this_user=User.objects.get(first_name=request.session['first_name'])
    context = {
            'all_users':User.objects.all(),
            'all_wishes':Wish.objects.all(),
            'current_user':this_user
        }
    return render(request,"wishes.html",context)

def edit_wishes(request , wish_id):
    this_wish=Wish.objects.get(id=wish_id)
    context={"this_wish":this_wish}
    return render(request,"edit_wishes.html",context)

def process_edit_wishes(request , wish_id):
    this_wish=Wish.objects.get(id=wish_id)
    errors = Wish.objects.basic_validator_edit_wish(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/wishes/edit/{this_wish.id}')
    this_wish=Wish.objects.get(id=wish_id)
    context={"this_wish":this_wish}
    return render(request,"edit_wishes.html",context)

def create_wish(request):
    this_user=User.objects.get(first_name=request.session['first_name'])
    context = {
            'current_user':this_user}
    return render(request,'new_wish.html',context)

def process_new_wish(request):
    errors = Wish.objects.basic_validator_new_wish(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        new_item=request.POST['new_item']
        new_desc=request.POST['new_desc']
        this_user=User.objects.get(first_name=request.session['first_name'])
        new_wish=Wish.objects.create(item=new_item,desc=new_desc,user=this_user)
        return redirect('/wishes')
            
    
def wishes_stats(request):
    return render(request,'wishes_stats.html')
    
def remove_wish(request , wish_id):
    wish_remove=Wish.objects.get(id=wish_id)
    wish_remove.delete()
    return redirect('/wishes')
    
def clear(request):
    request.session.clear()
    return redirect('/')
    




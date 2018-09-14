from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
import re
from .models import *
from django.contrib import auth
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def sign_in(request):
    print(User.objects.all())
    return render(request, 'handy_helper/sign_in.html')

def reg_process(request):
    found_users = User.objects.filter(email =request.POST['email'] )
    print('reg_process here!!')
    error=False
    if len(request.POST['first_name']) < 2:
        messages.error(request,"Name must be greater than two letters")
        error=True
    if len(request.POST['last_name']) < 2:
        messages.error(request,"Last name must be greater than two letters")
        error=True
    if len(request.POST['password'])  <= 8:
        messages.error(request,"Password must be greater than eight characters")
        error=True
    if request.POST['password'] != request.POST['c_password']:
        messages.error(request,"Password confirmation must match")
        error=True
    if len(found_users) > 0:
        messages.error(request,"That email is already registered. Try to sign in!")
        error=True
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,"Email must be valid")
        error=True
    if error:
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        u = User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'], email = request.POST['email'], password = password)
        request.session['id'] = u.id
        return redirect('/jobs')
        print("^"*80,"^"*40)
        print('Log_process here!!')

def sign_in_process(request):
    user = User.objects.filter( email = request.POST['email'])    
    if len(user) > 0:
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id'] = user.id
            return redirect('/jobs')
        else:
            messages.error(request,"Try again, your email or password is incorrect")
            return redirect('/')
    else:
        messages.error(request,"Try again, your email or password is incorrect")
        return redirect('/')


def jobs(request):
    se_user = User.objects.filter( id = request.session['id'])
    u = User.objects.get(id= request.session['id'])
    context={
        'jobs' : Job.objects.filter(user__id=u.id ),
        'user' : User.objects.all(),
        'person' : User.objects.filter( id = request.session['id']),
        'others_jobs' : Job.objects.all().exclude(user__id=u.id ),
    }
    print(u.email)
    print(request.session['id'])
    return render(request,'handy_helper/dashboard.html',context,u)

def logout(request):
    auth.logout(request)
    return redirect('/')

def join(request,id):
    this_user = User.objects.get(id=request.session['id'])
    curr_job = Job.objects.filter(id=id)[0]
    curr_job.user_id = this_user.id
    curr_job.save()
    return redirect('/jobs')

def back(request):
    return redirect('/jobs')

def delete(request,id):
    d_job = Job.objects.get(id = id)
    d_job.delete()
    return redirect('/jobs')

def job_post(request):
    se_user = User.objects.filter( id = request.session['id'])
    u = se_user[0]
    if request.POST['job'] == "" or request.POST['location'] == "" or request.POST['description'] == "":
        messages.error(request,"Fields should not be empty!")
        return redirect('/add_job')
    if request.method != "POST":
        return redirect('/')
    else:
        error=False
        if len(request.POST['job']) < 3:
            messages.error(request,"Give your job a real name, Patrick!")
            error=True
        if len(request.POST['location']) < 1:
            messages.error(request,"Give us your jobs location, Patrick!")
            error=True
        if len(request.POST['description']) < 10:
            messages.error(request,"Give us your jobs description, Patrick!(Greater than 10 characters)")
            error=True

        if error:
            return redirect('/add_job')

        else:
            this_user = User.objects.get(id=request.session['id'])
            curr_job = Job.objects.create(job= request.POST['job'],  location = request.POST['location'],job_creater=request.session['id'],description = request.POST['description'],user_id=0)
            print(u.email)
            return redirect('/jobs')

def add_job(request):
    se_user = User.objects.filter( id = request.session['id'])
    u = se_user[0]
    context={
        'jobs' : Job.objects.all(),
        'user' : User.objects.all(),
        'person' : User.objects.filter( id = request.session['id']),
        'others_jobs' : Job.objects.filter().exclude(user__id = u.id),
        'u' : User.objects.filter( id = request.session['id']),
    }
    return render(request,'handy_helper/add_job.html',context,u)

def cancel(request, id):
    this_user = User.objects.get(id=request.session['id'])
    curr_job = Job.objects.filter(id=id)[0]
    curr_job.user_id= 0
    curr_job.save()
    return redirect('/jobs')

def done(request,id):
    d_job = Job.objects.get(id = id)
    d_job.delete()
    return redirect('/jobs')

def show_job(request,id):
    job_1=Job.objects.filter(id=id)[0]
    context={
        'job' : Job.objects.filter(id=id)
    }
    print(job_1.job_creater)
    return render(request,'handy_helper/show_job.html', context)

def edit_job(request,id):
    context={
        'job' : Job.objects.filter(id=id)
    }
    return render(request, 'handy_helper/edit_job.html',context)


def edit_job_process(request,id):
    context={
        'jobs': Job.objects.filter(id=id)
    }
    if request.method != 'POST':
        return redirect('/')
    else:
        edited_job = Job.objects.get(id=id)
        edited_job.job = request.POST['job']
        edited_job.location = request.POST['location']
        edited_job.description = request.POST['description']
        edited_job.save()
        return redirect('/jobs')

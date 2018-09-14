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

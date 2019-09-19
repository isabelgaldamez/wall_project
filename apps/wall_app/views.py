from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Message, Comments
import bcrypt

def index(request):
    return render(request,'wall_app/index.html')

def registration(request):
    errors = User.objects.register_user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="r"+key)

            # messages.error(request, value)
        return redirect ('/')

    if request.method == 'POST':
        # encode the password
        pw_hash = bcrypt.hashpw(request.POST['new_password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['reg_email'], password = pw_hash)

    return redirect('/')

def auth_user(request):
    login_errors = User.objects.login_user_validator(request.POST) 
    if len(login_errors) > 0:
        for key, value in login_errors.items():
            messages.error(request, value, extra_tags="l"+key)
            # messages.error(request, value)
        return redirect ('/')
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['user_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/success')
            else: 
                print('Incorrect password, try again')
                return redirect('/')
    return redirect('/')

def user_logged(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        all_messages = Message.objects.all()
        all_comments = Comments.objects.all()
        user = User.objects.get(id = request.session['user_id'])

        context = {
            'logged_user_info' : user,
            'messages'  : all_messages,
            'comments' : all_comments,
        }
        return render(request, 'wall_app/user_wall.html', context)

def new_post(request):
    if request.method == 'POST':
        current_user = User.objects.get(id = request.session['user_id'])
        recent_post = Message.objects.create(message = request.POST['new_post_desc'], user_id = current_user)
    return redirect('/success')

def post_comment(request):
    if request.method == 'POST':
        current_user = User.objects.get(id = request.session['user_id'])
        post_to_message = Message.objects.get(id = request.POST['message_id'])
        Comments.objects.create(comment = request.POST['post_comment'], user_id = current_user, message_id = post_to_message)
    return redirect('/success')

def delete_message(request):
    if request.method == 'POST':
        message_to_delete = Message.objects.get(id = request.POST['delete_post'])
        message_to_delete.delete()
    return redirect('/success')
        

def clear_session(request):
    del request.session['user_id']
    return redirect('/')
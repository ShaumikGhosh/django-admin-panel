from django.shortcuts import render, redirect
from django.views import View
from admin.forms import (
    AdminLoginForm,
    ChangePasswordForm,
    UserActionForm
)
from django.contrib.auth import login, authenticate, logout
import hashlib
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages

# class AdminDashboardRegister(View):
#
#     template_name = 'admin/auth/register.html'
#
#     def get(self, request):
#         return render(request, self.template_name)

def admin(request):
    return redirect('login')


class AdminDashboardLogin(View):

    template_name = 'admin/auth/login.html'

    def get(self, request):
        context = {}
        context['form'] = AdminLoginForm()
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        context['form'] = AdminLoginForm(request.POST)

        if context['form'].is_valid():

            # checking here if remember me option is selected .......

            if context['form'].cleaned_data.get('remember_me') is True:

                username = context['form'].cleaned_data.get('userCt', None)
                password = context['form'].cleaned_data.get('password', None)

                user = authenticate(user=username, password=password)
                if user:
                    if user.is_active is bool(True):
                        login(request, user)
                        response = redirect('index')
                        response.set_cookie('shaumikghosh',
                                            hashlib.sha512(user.username.encode()).hexdigest(),
                        max_age=60*60*48, httponly=True, samesite='Lax')
                        return response
                    else:
                        context['error_msg'] = 'Your account is suspended!'
                        return render(request, self.template_name, context)
                else:
                    context['error_msg'] = 'Invalid credentials provided!'
                    return render(request, self.template_name, context)

            # if remember me is not selected then  this action will perform .......

            else:

                username = context['form'].cleaned_data.get('userCt', None)
                password = context['form'].cleaned_data.get('password', None)

                user = authenticate(user=username, password=password)
                if user:
                    if user.is_active is bool(True):
                        login(request, user)
                        return redirect('index')
                    else:
                        context['error_msg'] = 'Your account is suspended!'
                        return render(request, self.template_name, context)
                else:
                    context['error_msg'] = 'Invalid credentials provided!'
                    return render(request, self.template_name, context)

        return render(request, self.template_name, context)


class AdminDashboardLogout(View):

    def get(self, request):
        if request.COOKIES.get('shaumikghosh'):
            logout(request)
            response = redirect('login')
            response.delete_cookie('shaumikghosh')
            return response
        else:
            logout(request)
            return redirect('login')


class AdminDashboardIndex(View):

    template_name = 'admin/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class AdminDashboardSettings(View):

    template_name = 'admin/settings.html'

    def get(self, request):
        context = {}
        context['form'] = ChangePasswordForm()
        context['users'] = User.objects.all().order_by('-id')
        context['actionForm'] = UserActionForm()
        context['loggedin'] = 0
        return render(request, self.template_name, context)

    def post(self, request):
        if 'change_password_button' in request.POST:
            context = {}
            context['form'] = ChangePasswordForm(request.POST)
            if context['form'].is_valid():
                if request.user.check_password(context['form'].cleaned_data.get('oldPassword', None)):
                    updateUser = User.objects.get(id=request.user.id)
                    updateUser.password = make_password(context['form'].cleaned_data.get('confirmPassword', None))
                    updateUser.save()
                    messages.success(request, "Password successfully updated, login again!",
                                     extra_tags="password_changed_success")
                    return redirect('login')
                else:
                    context['error_msg'] = "Old password verification failed!"
                    return render(request, self.template_name, context)
            return render(request, self.template_name, context)
        elif 'user_action_button' in request.POST:
            context = {}
            context['users'] = User.objects.all()
            context['form'] = ChangePasswordForm()
            context['actionForm'] = UserActionForm(request.POST)
            if context['actionForm'].is_valid():
                if context['actionForm'].cleaned_data.get('selectAction', None).__eq__('deactivate'):
                    if len(request.POST.getlist('checkedItems', None)).__gt__(0):
                        context['selected_value'] = request.POST.getlist('checkedItems', None)
                        for item in context['selected_value']:
                            usr = User.objects.get(id=item)
                            usr.is_active = False
                            usr.save()
                        context['operational_success_msg'] = 'Selected users have been deactivated!'
                        return render(request, self.template_name, context)
                    else:
                        context['operational_error_msg'] = 'Operational item must be selected!'
                        return render(request, self.template_name, context)
                elif context['actionForm'].cleaned_data.get('selectAction', None).__eq__('activate'):
                    if len(request.POST.getlist('checkedItems', None)).__gt__(0):
                        context['selected_value'] = request.POST.getlist('checkedItems', None)
                        for item in context['selected_value']:
                            usr = User.objects.get(id=item)
                            usr.is_active = True
                            usr.save()
                        context['operational_success_msg'] = 'Selected users have been activated!'
                        return render(request, self.template_name, context)
                    else:
                        context['operational_error_msg'] = 'Operational item must be selected!'
                        return render(request, self.template_name, context)
                elif context['actionForm'].cleaned_data.get('selectAction', None).__eq__('do_superuser'):
                    if len(request.POST.getlist('checkedItems', None)).__gt__(0):
                        context['selected_value'] = request.POST.getlist('checkedItems', None)
                        for item in context['selected_value']:
                            usr = User.objects.get(id=item)
                            usr.is_superuser = True
                            usr.save()
                        context['operational_success_msg'] = 'Selected users have become superuser!'
                        return render(request, self.template_name, context)
                    else:
                        context['operational_error_msg'] = 'Operational item must be selected!'
                        return render(request, self.template_name, context)
                elif context['actionForm'].cleaned_data.get('selectAction', None).__eq__('undo_superuser'):
                    if len(request.POST.getlist('checkedItems', None)).__gt__(0):
                        context['selected_value'] = request.POST.getlist('checkedItems', None)
                        for item in context['selected_value']:
                            usr = User.objects.get(id=item)
                            usr.is_superuser = False
                            usr.save()
                        context['operational_success_msg'] = 'Selected users have been undo from superuser!'
                        return render(request, self.template_name, context)
                    else:
                        context['operational_error_msg'] = 'Operational item must be selected!'
                        return render(request, self.template_name, context)
                elif context['actionForm'].cleaned_data.get('selectAction', None).__eq__('delete'):
                    if len(request.POST.getlist('checkedItems', None)).__gt__(0):
                        context['selected_value'] = request.POST.getlist('checkedItems', None)
                        for item in context['selected_value']:
                            usr = User.objects.get(id=item)
                            usr.delete()
                        context['operational_success_msg'] = 'Selected users have been deleted successfully!'
                        return render(request, self.template_name, context)
                    else:
                        context['operational_error_msg'] = 'Operational item must be selected!'
                        return render(request, self.template_name, context)
            else:
                print(context['actionForm'].errors)
            return render(request, self.template_name, context)
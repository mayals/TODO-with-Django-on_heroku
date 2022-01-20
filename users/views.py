from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView, UpdateView, DetailView
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from . models import Profile
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



#------ login ---------------
class UserLoginView(LoginView):
    success_url = reverse_lazy('todo:tasks')
    template_name = 'users/login.html'
    extra_context = {
        'title': 'To DO Tasks',
        'sub_title': 'log-in',
        }
# --------------------------------------



# --- logout --------#
class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
    extra_context = {
        'title': 'To DO Tasks',
        'sub_title': 'log-out',
    }
#------------------------------   # 



# --- register ----
class UserFormView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:UserLogin')
    initial = {'key': 'value'}
    extra_context = {
        'title': 'To DO Tasks',
        'sub_title': 'Register',
    }
    

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        form = self.form_class(initial=self.initial)
        context ={
            'form': form,
            'title': 'To DO Tasks',
            'sub_title': 'Register',
        }
        return render(request, self.template_name,context)
    
    
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, f'good job {user}, you are register successfuly')
            return redirect('users:UserLogin')
        
        
        context ={
            'form': form,
            'title': 'To DO Tasks',
            'sub_title': 'Register',
        }
        return render(request, self.template_name, context)
# -------------------------------------------------------------------#




# ---profile --------------------------------
@login_required(login_url='users:UserLogin')
def profile_view(request):
    profile = get_object_or_404(Profile, P_user=request.user)
    print(profile)
    context ={
        'profile' : profile ,
    }
    return render(request,'users/profile.html',context)
# -------------------------#




# -- profile edit -----------------#
@login_required(login_url='users:UserLogin')
def profile_user_edit(request):
    profile = get_object_or_404(Profile,P_user=request.user)
    if request.method == 'POST':
        user_edit_form= UserUpdateForm(instance=request.user,data=request.POST)
        profile_edit_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit = user_edit_form.save(commit=False)
            user_edit.username = request.user.username
            user_edit.save()
            profile_edit = profile_edit_form.save(commit=False)
            profile_edit.P_user = request.user
            profile_edit.save()
            messages.success( request,'you are successfully update your profile')              
            return redirect('todo:tasks')
    
    else:
        user_edit_form = UserUpdateForm(instance=request.user)
        profile_edit_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_edit_form': user_edit_form,
        'profile_edit_form': profile_edit_form,

    }   
    return render(request,'users/profile_user_edit.html',context)
# -------------------------------------------------------








# class ProfileDetailView(DetailView):

#     template_name = "users/profile.html"
#     model = Profile

#     def get_context_data(self, instance,** kwargs):
#         context = super(ProfileDetailView, self).get_context_data(**kwargs)
#         context['P_user'] = instance.user
#         return context



# class ProfileUpdateView(UpdateView):
   
#     def user_passes_test(self, request):
#         if request.user.is_authenticated():
#             self.object = self.get_object()
#             return self.object.user == request.user
#         return False


#     def dispatch(self, request, *args, **kwargs):
#         if not self.user_passes_test(request):
#             return redirect_to_login(request.get_full_path())
#         return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)
           

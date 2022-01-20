from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView
from .models import Task
from django.utils import timezone
from .forms import AddTask,EditTask
from django.contrib import messages
from django.contrib.auth.decorators import login_required




@login_required(login_url='users:UserLogin')
def tasks(request):
    tasks = Task.objects.filter(T_user=request.user)
    
    if request.method == 'POST':
        form = AddTask(request.POST)
        if 'T_name' in request.POST:
            T_name = request.POST['T_name']
            if T_name:
                if form.is_valid():
                        T_name = form.cleaned_data['T_name']  
                        if T_name:
                            newtask= form.save(commit=False)
                            newtask.T_status = False
                            newtask.T_user = request.user
                            newtask= form.save()
                
                else: 
                        print('novalid')
                        # Get the text that was entered in `T_name`
                        T_name = request.POST.get("T_name")
                        length_of_T_name = len(T_name)
                        print(length_of_T_name)
                        # Simply send your own message
                        messages.warning(request, f"Error: maximum length limit is 30 characters (it has {length_of_T_name}).")
                
                return redirect('todo:tasks')
                  
            else:
                messages.warning(request, 'please add task.')
                return redirect('todo:tasks')
    else:
        form = AddTask()    
  
    context = {
        'tasks': tasks,
        'tasks_done': tasks.filter(T_status=True),
        'tasks_not_done': tasks.filter(T_status=False),
        'form' : form ,
        'title': 'To DO Tasks',
        'sub_title': 'index',
    }
    return render(request, 'todo/index.html', context)
# ----------------------------------------------------




# ---change status -- done/not done ---#
def change_status(request, task_id):
    tasks = Task.objects.all()
    task = get_object_or_404(Task,id=task_id)
    if task.T_status == False:
        task.T_status = True
        task.save()
    
    elif task.T_status == True :
        task.T_status = False
        task.save()

    return redirect('todo:tasks')
# ----------------------------------------- 




# --- task delete ---------------------------
@login_required(login_url='users:UserLogin')
def task_delete(request, task_id):
    task = get_object_or_404(Task,id=task_id)
    task.delete()
    return redirect('todo:tasks')
# ---------------------------




#  all tasks_not_done_delete ----
@login_required(login_url='users:UserLogin')
def tasks_not_done_delete(request):
    tasks = Task.objects.filter(T_status=False)
    tasks.delete()
    return redirect('todo:tasks')
# ---------------------------



#  all tasks_done_delete ----
@login_required(login_url='users:UserLogin')
def tasks_done_delete(request):
    tasks = Task.objects.filter(T_status=True)
    tasks.delete()
    return redirect('todo:tasks')
# ---------------------------





# ----task_edit ---- need complate !------------------
@login_required(login_url='users:UserLogin')
def task_edit(request,task_id):
    if request.method == 'POST':
       
        T_name = request.POST.get('T_name_edit')
        if T_name:
            length_of_T_name = len(T_name)
            print(length_of_T_name)
            if length_of_T_name > 30:
                # Simply send your own message
                messages.warning(request, f"Error: maximum length limit is 30 characters (it has {length_of_T_name}).")
                return redirect('todo:tasks')
            
            else:
                task_id = request.POST.get('edit_id')
                T_name = request.POST.get('T_name_edit')
                T_user = request.user
                T_published = timezone.now()
                task = Task(id=task_id, T_name=T_name,T_user=T_user, T_published=T_published)
                task.save()
                messages.success(request, 'edit successfully.')
                return redirect('todo:tasks')
   
    else:
        return redirect('todo:tasks')
# ----------------------------------------------

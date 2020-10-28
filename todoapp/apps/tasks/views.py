from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from django.views.generic import ListView, View, DetailView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from django.db.models import Q

# for smtp
from django.core.mail import send_mail
from django.conf import settings

from tasks.models import TodoItem, Publisher
from tasks.forms import AddTaskForm, TodoItemExportForm

from taggit.models import Tag


def get_task_by_id(task_id):
    try:
        task = TodoItem.objects.get(id = task_id)
    except:
        return False
    return task


def filter_tags(tags_by_task):
    new_lst = []
    for i in tags_by_task:
        for j in i:
            if j not in new_lst:
                new_lst.append(j)
    return new_lst


def filter_tasks(tasks, tag):
    filtred_tasks = []
    for task in tasks:
        if tag in task['tags']:
            filtred_tasks.append(task['id'])
    return filtred_tasks


@login_required
def index(request):
    return HttpResponse('hello')


'''
def task_list(request):
    tasks = TodoItem.objects.all()
    return render(request, 'tasks/list.html', {
        'tasks': tasks
    })
'''

# страница доступна только для авторизованных пользователей
# class TaskListView(LoginRequiredMixin, ListView):
class TaskListView(LoginRequiredMixin, ListView):
    model = TodoItem
    context_object_name = 'tasks'
    template_name = 'tasks/list.html'

    def get_queryset(self):
        u = self.request.user
        if u.is_anonymous:
            return []
        return u.tasks.all()
    
    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        for task in user_tasks:
            tags.append(list( task.tags.all() ))
        context['tags'] = filter_tags(tags)
        return context


'''
def delete_task(request, task_id):
    task = get_task_by_id(task_id)
    if not task:
        return Http404('Task not found')

    task.delete()
    return HttpResponseRedirect(reverse('tasks:list'))
'''

class DeleteTaskView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'task_id' in kwargs:
            task = get_task_by_id(kwargs['task_id'])
        else:
            return Http404('Wrong reqest')

        if not task:
            return Http404('Task not found')
        task.delete()
        messages.success(request, "Задача удалена")
            # messages.error(request, "Задача удалена")
            # messages.info(request, "Задача удалена")
            # messages.warning(request, "Задача удалена")
        
        if 'tag_slug' in kwargs:
            # посмотреть сколько задач с этим тагом у этого пользователя
            u = self.request.user
            count_tags = len(TodoItem.objects.filter(tags__slug__in=[kwargs['tag_slug']]).filter(owner=u))
            if count_tags:
                return redirect(reverse(f'tasks:list_by_tag', args=[kwargs['tag_slug']]))

        return redirect(reverse(f'tasks:list'))



'''
def complete_task(request, task_id):
    task = get_task_by_id(task_id)
    if not task:
        return HttpResponse('ERROR')
    
    task.is_completed = True
    task.save()
    return HttpResponse('OK')
'''


class CompleteTaskView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'task_id' in kwargs:
            task = get_task_by_id(kwargs['task_id'])
        else:
            return Http404('Wrong reqest')
        
        task = get_task_by_id(kwargs['task_id'])
        if not task:
            return Http404('Task not found')
    
        task.is_completed = True
        task.save()
        return HttpResponse('OK')




'''
def create_task(request):
    # Вариант, для не модельной формы
    # if request.method == 'POST':
    #     form = AddTaskForm(request.POST)
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         desc = cd['description']
    #         t = TodoItem(description=desc)
    #         t.save()
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:list'))
    else:
        form = AddTaskForm()
    return render(request, 'tasks/create.html', {
        'form': form,
    })
'''


class CreateTaskView(LoginRequiredMixin, View):
    def my_render(self, request, form):
        return render(request, "tasks/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AddTaskForm(request.POST)
        if form.is_valid():
            # form.save()
            # подмешаем юзера в форму
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            # чтобы сохранить теги (по дефолту поля m2m не сохраняются при commit=False)
            form.save_m2m()
            return HttpResponseRedirect(reverse('tasks:list'))


        return self.my_render(request, form)

    def get(self, request, *args, **kwargs):
        form = AddTaskForm()
        return self.my_render(request, form)


# def add_task(request):
#     if request.method == 'POST':
#         desc = request.POST['description']
#         if len(desc):
#             t = TodoItem(description=desc)
#             t.save()
#     return HttpResponseRedirect(reverse('tasks:create_task'))


class TaskDetailsView(LoginRequiredMixin, DetailView):
    # объект будет доступен по имени object
    model = TodoItem
    template_name = 'tasks/details.html'
    
    # для отправки сообщений:
    # def get_context_data(self, **kwargs):
    #     context = super(TaskDetailsView, self).get_context_data(**kwargs)
    #     messages.info(self.request, 'details!!')
    #     return context


class TaskEditView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        t = TodoItem.objects.get(id=pk)
        form = AddTaskForm(request.POST, instance=t)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("tasks:list"))

        return render(request, "tasks/edit.html", {"form": form, "task": t})

    def get(self, request, pk, *args, **kwargs):
        t = TodoItem.objects.get(id=pk)
        form = AddTaskForm(instance=t)
        return render(request, "tasks/edit.html", {"form": form, "task": t})


class TaskExportView(LoginRequiredMixin, View):
    def generate_body(self, user, priorities, tag_slug=None):
        q = Q()
        if priorities['prio_high']:
            q = q | Q(priority=TodoItem.PRIORITY_HIGH)
        if priorities["prio_med"]:
            q = q | Q(priority=TodoItem.PRIORITY_MEDIUM)
        if priorities["prio_low"]:
            q = q | Q(priority=TodoItem.PRIORITY_LOW)

        body = 'Ваши задачи и приоритеты:\n'

        if tag_slug:
            body += f'С тегом {tag_slug}\n'
            tasks = TodoItem.objects.filter(tags__slug__in=[tag_slug]).filter(owner=user).filter(q).all()
        else:
            tasks = TodoItem.objects.filter(owner=user).filter(q).all()

        for t in list(tasks):
            if t.is_completed:
                body += f'[x] {t.description} ({ t.get_priority_display() })\n'
            else:
                body += f"[ ] {t.description} ({t.get_priority_display()})\n"
        return body
    
    def post(self, request, *args, **kwargs):
        form = TodoItemExportForm(request.POST)
        if form.is_valid():
            email = request.user.email
            if 'tag_slug' in kwargs:
                body = self.generate_body(request.user, form.cleaned_data, kwargs['tag_slug'])
            else:
                body = self.generate_body(request.user, form.cleaned_data)
            send_mail("Задачи", body, settings.EMAIL_HOST_USER, [email])
            messages.success(
                request, "Задачи были отправлены на почту %s" % email)
        else:
            messages.error(request, "Что-то пошло не так, попробуйте ещё раз")
        return HttpResponseRedirect(reverse("tasks:list"))

    def get(self, request, *args, **kwargs):
        form = TodoItemExportForm()
        if 'tag_slug' in kwargs:
            return render(request, "tasks/export.html", {"form": form, 'tag': kwargs['tag_slug']})
        return render(request, "tasks/export.html", {"form": form})


def tasks_by_tag(request, tag_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    tags_lst = []
    for t in tasks:
        tags_lst.append(list(t.tags.all()))
    
    tags_dict = {t.description: tag_lst for t, tag_lst in zip(tasks, tags_lst)}
    all_tags = filter_tags(tags_lst)

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        tasks = tasks.filter(tags__in=[tag])
    
    
    return render(request, 'tasks/list_by_tag.html', {
        'tag': tag,
        'tasks': tasks,
        'all_tags': all_tags,
        'tags_dict': tags_dict,
    })


class PublisherView(ListView):
    model = Publisher
    context_object_name = 'publishers'
    template_name = 'tasks/publisher.html'

    # достаём подмножество
    def get_queryset(self):
        if 'id' in self.kwargs:
            self.publisher = get_object_or_404(Publisher, id=self.kwargs['id'])
            return [self.publisher]
        else:
            return Publisher.objects.all()

    # расширение контекста
    def get_context_data(self, **kwargs):
        context = super(PublisherView, self).get_context_data(**kwargs)
        context['tasks'] = TodoItem.objects.all()
        return context

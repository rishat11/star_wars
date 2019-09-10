from django.shortcuts import render
from .forms import RecruitForm
from django.http import HttpResponse, HttpResponseRedirect as redirect
from django.urls import reverse
from .models import HandOfShadowTask, TaskResult, Recruit, Sith
from django.core.mail import send_mail


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        return HttpResponse("405")


def siths(request):
    siths = Sith.objects.all()
    return render(request, 'siths.html', {'siths': siths})


def sith_page(request, sith_id):
    recruits = Recruit.objects.filter(sith_hand_of_shadow__isnull=True)
    results = []
    for recruit in recruits:
        results.append(recruit.result)
    answers = zip(recruits, results)
    return render(request, 'siths_page.html', {'answers': answers, 'sith_id': sith_id})


def recruit_page(request):
    if request.method == 'POST':
        form = RecruitForm(request.POST)
        if form.is_valid():
            recruit = form.save()
            return redirect(reverse('main:questions', args=[recruit.id]))
        else:
            return render(request, 'recruit_form.html', {'form': form})
    elif request.method == 'GET':
        form = RecruitForm()
        return render(request, 'recruit_form.html', {'form': form})
    else:
        return HttpResponse("405")


def questions_page(request, recruit_id):
    task = HandOfShadowTask.objects.all()
    if len(task) == 0:
        return render(request, 'task_is_not_created.html')
    if request.method == 'GET':
        questions = task[0].list_of_questions.split('\n')
        return render(request, 'questions.html', {'questions': questions, 'recruit_id': recruit_id})
    elif request.method == 'POST':
        result = TaskResult()
        answers = request.POST.getlist('answers')
        result.list_of_questions = task[0].list_of_questions
        result.list_of_answers = '\n'.join(answers)
        recruit = Recruit.objects.get(id=recruit_id)
        result.recruit = recruit
        result.save()
        return redirect(reverse('main:index'))
    else:
        return HttpResponse('405')


def make_hand_of_shadow(request, recruit_id, sith_id):
    hand_limit = 3
    recruit = Recruit.objects.get(id=recruit_id)
    sith = Sith.objects.get(id=sith_id)
    if sith.hand_of_shadow.count() >= hand_limit:
        return render(request, 'hand_of_shadow_limit_exceeded.html')
    send_mail('Зачисление Рукой Тени',
              'Поздравляем Вы зачислены Рукой Тени к {} с планеты'.format(sith.name, sith.planet),
              'sith@orden.com',
              [recruit.email],
              fail_silently=False)
    recruit.sith_hand_of_shadow.add(sith)
    recruit.save()
    return redirect(reverse('main:index'))


def hand_amount(request):
    siths = Sith.objects.all()
    return render(request, 'hand_amount.html', {'siths': siths})


def more_than_one_hand(request):
    siths = Sith.objects.all()
    result = []
    for sith in siths:
        if sith.hand_of_shadow.count() > 1:
            result.append(sith)
    return render(request, 'more_than_one_hand.html', {'siths': result})

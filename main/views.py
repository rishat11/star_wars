from django.shortcuts import render
from .forms import RecruitForm
from django.http import HttpResponse, HttpResponseRedirect as redirect
from django.urls import reverse
from .models import Answer, Question, Recruit, Sith
from django.core.mail import send_mail
from django.db.models import Count


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        return HttpResponse("405")


def siths(request):
    if request.method == 'GET':
        siths = Sith.objects.all()
        return render(request, 'siths.html', {'siths': siths})
    else:
        return HttpResponse("405")


def sith_page(request, sith_id):
    if request.method == 'GET':
        recruits = Recruit.objects.filter(sith_hand_of_shadow__isnull=True).prefetch_related('answer')
        return render(request, 'siths_page.html', {'recruits': recruits, 'sith_id': sith_id})
    else:
        return HttpResponse("405")


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
    questions = Question.objects.all()
    if questions.count() == 0:
        return render(request, 'task_is_not_created.html')
    if request.method == 'GET':
        answers = []
        for question in questions:
            answer = Answer()
            answer.question = question
            answers.append(answer)
        return render(request, 'questions.html', {'answers': answers, 'recruit_id': recruit_id})
    elif request.method == 'POST':
        for question in questions:
            answer = Answer()
            answer.recruit = Recruit.objects.get(id=recruit_id)
            answer.question = question
            answer.text = request.POST.get(str(question.id), False)
            answer.save()
        return redirect(reverse('main:index'))
    else:
        return HttpResponse('405')


def make_hand_of_shadow(request, recruit_id, sith_id):
    if request.method == 'GET':
        hand_limit = 3
        recruit = Recruit.objects.get(id=recruit_id)
        recruit_hand_count = recruit.sith_hand_of_shadow.all().count()
        sith = Sith.objects.get(id=sith_id)
        if recruit_hand_count >= hand_limit:
            return render(request, 'hand_of_shadow_limit_exceeded.html')
        send_mail('Зачисление Рукой Тени',
                  'Поздравляем Вы зачислены Рукой Тени к {} с планеты {}'.format(sith.name, sith.planet.name),
                  'sith@orden.com',
                  [recruit.email],
                  fail_silently=False)
        recruit.sith_hand_of_shadow.add(sith)
        recruit.save()
        return redirect(reverse('main:index'))
    else:
        return HttpResponse('405')


def hand_amount(request):
    if request.method == 'GET':
        siths = Sith.objects.all()
        return render(request, 'hand_amount.html', {'siths': siths})
    else:
        return HttpResponse('405')


def more_than_one_hand(request):
    if request.method == 'GET':
        siths = Sith.objects.annotate(hands_count=Count('hand_of_shadow')).filter(hands_count__gt=1)
        return render(request, 'more_than_one_hand.html', {'siths': siths})
    else:
        return HttpResponse('405')

# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from django.forms.models import modelformset_factory, inlineformset_factory
import random
import forms
from models import Interview, InterElem
import pdb

from models import Interview, InterElem, DoneInterview


def message(request, mess_text):
    """
    Для отображения сообщений
    """
    return render(request, 'interview/message.html', {'title': mess_text})


def list_interviews(request):
    """
    Выводит список всех существующих опросов
    """
    c_dict = {}
    c_dict['title'] = 'Список всех опросов:'
    c_dict['user'] = auth.get_user(request)
    c_dict['interviews'] = Interview.objects.all()
    return render(request, 'interview/listinterviews.html', c_dict)


# def edit_interview2(request, interview_id):
#     """
#     Тут будет страница для редактирования конкретного опроса - сейчас не используется
#     """
#     c_dict = {}
#     interview = get_object_or_404(Interview, pk=interview_id)
#     c_dict['interview'] = interview
#     return render(request, "interview/edit_interview.html", c_dict)


def edit_interview(request, interview_id):
    """
    Тут попробуем через наборы модельных форм modelformset_factory
    """
    interview = get_object_or_404(Interview, pk=interview_id)
    ElemFormset = modelformset_factory(InterElem, exclude=('interview',), extra=1, can_delete=True)
    c_dict = {}
    c_dict.update(csrf(request))
    c_dict['title'] = 'Редактируем опрос'
    if request.method == 'POST':
        inter_form = forms.FormEditInterview(request.POST, instance=interview)
        elem_formset = ElemFormset(request.POST,
                                   queryset=InterElem.objects.filter(interview=interview).order_by('position'),
                                   prefix='elems')

        if elem_formset.is_valid() and inter_form.is_valid():
            inter_form.save()

            # тут нужно еще досохранить объект интервью в каждой форме
            forms_list = elem_formset.save(commit=False)

            # удалим формы, помеченные для удаления (checkbox)
            for item in elem_formset.deleted_objects:
                item.delete()

            # досохраняем объект interview для правильной внешней ссылки
            for item in forms_list:
                item.interview = interview
                item.save()

            return HttpResponseRedirect(reverse('edit_interview', args=(interview_id,)))
    else:
        inter_form = forms.FormEditInterview(instance=interview)
        elem_formset = ElemFormset(queryset=InterElem.objects.filter(interview=interview).order_by('position'),
                                   prefix='elems')
    c_dict['inter_form'] = inter_form
    c_dict['elem_formset'] = elem_formset
    return render(request, "interview/editinterview.html", c_dict)


def pass_interview(request, interview_id):
    """
    Функция-представление для голосования по конкретному опросу interview_id
    """
    interview = Interview.objects.get(pk=interview_id)
    # выбираем элементы конкретного опроса
    elems = interview.interelem_set.order_by('position')

    if not elems:
        return render(request, 'interview/message.html',
                      {'title': 'Вопросы пока не готовы. Спасибо за понимание)'})

    # тут надо проверить access в interview (нужно авторизироваться или куки)
    user = auth.get_user(request)
    if interview.access > 0 and user.is_anonymous():
        return render(request, 'interview/message.html',
                      {'title': 'Только для зарегистрированных пользователей'})

    if user.is_anonymous():
        # создадим id для уникальных юзеров
        user.id = random.randrange(100000001, 101000000)
        # проверяем не голосовал ли он ранее по куке
        if ('inter_%s' % interview_id) in request.COOKIES:
            return render(request, 'interview/message.html',
                          {'title': 'Извините, но вы уже прошли этот опрос'})
    else:
        # проверим есть ли у юзера ответ на верхний вопрос текущего опроса
        if DoneInterview.objects.filter(user_id=user.id, interelem=elems[0]).exists():
            return render(request, 'interview/message.html',
                          {'title': 'Извините, но вы уже прошли этот опрос'})

    # готовим context для шаблона
    c_dict = {}
    c_dict['interview_id'] = interview_id
    c_dict['title'] = 'Doing interview'
    c_dict.update(csrf(request))

    if request.method != 'POST':
        form = forms.FormInterview(elems)
        c_dict['form'] = form
    else:
        form = forms.FormInterview(elems, request.POST)
        c_dict['form'] = form
        if form.is_valid():
            cd = form.cleaned_data

            # тут сохраняем введенные юзером данные по перечню элементов опроса
            # можно потом вынести в FormInterview.save()
            for key in cd:
                interelem = get_object_or_404(InterElem, pk=int(key))
                resp = cd[key]
                # если данные ответа - мультиселект
                if isinstance(resp, list):
                    # pdb.set_trace()
                    resp = ', '.join(resp)
                # если checkbox
                elif isinstance(resp, bool):
                    resp = 'да' if resp else 'нет'
                user_meta = request.META['HTTP_USER_AGENT']
                try:
                    interelem.doneinterview_set.create(user_id=user.id, resp=resp, user_meta=user_meta)
                except:
                    raise Http404('Не удалось сохранить ваши данные. Попробуйте еще разок.')
            response = render(request, 'interview/message.html', {'title': 'Спасибо, вы успешно прошли опрос'})

            # если аноним, то ставим ему куку
            if user.is_anonymous():
                response.set_cookie('inter_%s' % interview_id, 'done')
            return response
            # return HttpResponseRedirect(reverse('pass_interview', args=(interview_id, )))
    return render(request, 'interview/passinterview.html', c_dict)


# закрываем доступ для обычных (не staff) юзеров с переходом на список опросов
#@permission_required('interview.add_interview', login_url='/interview/')
def interview_results(request, interview_id):
    """
    Вывод результатов конкретного опроса
    """
    c_dict = {}
    interview = get_object_or_404(Interview, pk=interview_id)
    c_dict['title'] = 'А вот и результаты голосования по опросу:'
    c_dict['descr'] = interview.description

    # оборачиваем list, чтобы выполнить запрос именно в этом месте
    elems = list(interview.interelem_set.order_by('position'))

    if elems:
        # выберем всех юзеров, которые голосовали по конкретному опросу
        # done_interview_users = DoneInterview.objects.filter(interelem__in=list(elems)).distinct('user_id')
        # distinct - почему-то не заработал
        done_interview_users = DoneInterview.objects.filter(interelem__in=elems)

        # здесь будем сохранять уникальных голосовавших пользователей
        users = []
        for done_interview_user in done_interview_users:
            if done_interview_user.user_id not in users:
                users.append(done_interview_user.user_id)

        resps = []
        questions = []

        # формируем список вопросов-элементов интервью
        for elem in elems:
            questions.append(elem.text_before_elem)

        # проходим по перечню объектов результатов голосования с уникальными юзерами.
        # Это для того, чтобы отобразить в шаблоне таблицу, растущую вниз.
        for user in users:
            user_resps = []
            for elem in elems:

                # нужно перехватить исключение, т.к. вопрос-элемент мог добавиться к опросу после
                # голосования каким-либо юзером и тогда просто не будет нужного объекта-результат голосования.
                try:
                    elem_response = DoneInterview.objects.get(user_id=user, interelem=elem)
                    tmp = elem_response.resp
                except Exception:
                    tmp = ''
                user_resps.append(tmp)
            # добавляем в список кортеж ('юзер', [ответы...])
            resps.append((user, user_resps))

        c_dict['questions'] = questions
        c_dict['resps'] = resps
    return render(request, 'interview/interviewresults_new.html', c_dict)


# def interview_results_new(requerst, interview_id):
#     """
#     Обновленная функция interview_result (см. выше). Тут немного подругому обращаемся к базе данных.
#     """
#     c_dict = {}
#     interview = get_object_or_404(Interview, pk=interview_id)
#     elems = list(interview.interelem_set.order_by('position'))
#
#     # тут список объектов-ответов всех юзеров по данному интервью
#     all_resps = list(DoneInterview.objects.filter(interelem__in=elems))
#
#     # выберем список юзеров
#     users_list = []
#     for item in all_resps:
#         if item.user_id not in users_list:
#             users_list.append(item.user_id)
#
#     # для каждого юзера вытащим нужный ответ
#     for item in all_resps:
#         pass
#
#     return render(requerst, 'interview/interviewresults_new.html', c_dict)


def add_interview(request):
    """
    Тут добавляем новый опрос в базу
    """
    c_dict = {}
    c_dict.update(csrf(request))
    c_dict['title'] = 'Добавляем опрос'
    if request.POST:
        inter_form = forms.FormEditInterview(request.POST)
        if inter_form.is_valid():
            interview_id = inter_form.save()
            # return redirect('interview/%s/edit' % interview_id)
            return HttpResponseRedirect(reverse('edit_interview', args=(interview_id.id, )))
    else:
        inter_form = forms.FormEditInterview()
    c_dict['inter_form'] = inter_form
    return render(request, 'interview/editinterview.html', c_dict)

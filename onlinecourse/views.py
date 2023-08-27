from django.shortcuts import render
from django.http import HttpResponseRedirect
# <HINT> Import any new Models here
from .models import Choice, Course, Enrollment, Submission, Pergunta
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.

from django.shortcuts import render, redirect
from .models import Pergunta, Resposta

def lista_perguntas(request):
    perguntas = Pergunta.objects.all()

    if request.method == 'POST':
        respostas_selecionadas = request.POST.getlist('respostas')
        # Processar as respostas selecionadas aqui (por exemplo, marcar as respostas corretas)

        return redirect('onlinecourse:lista_perguntas')  # Redirecionar após processamento

    return render(request, 'onlinecourse/lista_perguntas.html', {'perguntas': perguntas})


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# CourseListView
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


# <HINT> Create a submit view to create an exam submission record for a course enrollment,
# you may implement it based on following logic:
         # Get user and course object, then get the associated enrollment object created when the user enrolled the course
         # Create a submission object referring to the enrollment
         # Collect the selected choices from exam form
         # Add each selected choice object to the submission object
         # Redirect to show_exam_result with the submission id
#def submit(request, course_id):


# Função para coletar as escolhas selecionadas do formulário de exame
def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)
    return submitted_answers

# Função para processar a submissão do exame
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    # Obter o registro de matrícula associado
    enrollment = Enrollment.objects.get(user=user, course=course)

    if request.method == "POST":
        # Criar um registro de submissão associado à matrícula
        submission = Submission.objects.create(enrollment=enrollment)

        # Coletar as escolhas selecionadas do formulário de exame
        selected_choices = extract_answers(request)

        # Adicionar cada escolha selecionada ao registro de submissão
        for choice_id in selected_choices:
            choice = Choice.objects.get(id=choice_id)
            submission.choices.add(choice)

        # Redirecionar para a visualização de resultados do exame
        return redirect(reverse('onlinecourse:show_exam_result', args=(course_id, submission.id)))

    # Renderizar o template exam_submission_form.html
    return render(request, 'onlinecourse/exam_submission_form.html', {'course': course})



#def show_exam_result(request, course_id, submission_id):

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Get the selected choice ids from the submission record
    selected_choice_ids = submission.choices.values_list('id', flat=True)

    # Calculate the score
    total_score = 0
    question_results = []

    for question in course.lesson_set.all():  # Assuming each lesson has a question
        correct_choice_ids = question.choice_set.filter(is_correct=True).values_list('id', flat=True)
        selected_correct = all(choice_id in selected_choice_ids for choice_id in correct_choice_ids)
        score = question.question_grade if selected_correct else 0

        total_score += score
        question_results.append({'question': question, 'selected_correct': selected_correct, 'score': score})

    # Check if the learner passed the exam
    passing_score = 70  # Set your passing score here
    passed_exam = total_score >= passing_score

    # Render the exam result template
    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'submission': submission,
        'question_results': question_results,
        'total_score': total_score,
        'passed_exam': passed_exam,
    })



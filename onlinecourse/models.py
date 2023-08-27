from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Modelo para instrutores
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Referência ao modelo de usuário do Django
        on_delete=models.CASCADE,  # Se o usuário for excluído, exclua também este instrutor
    )
    full_time = models.BooleanField(default=True)  # Indica se é um instrutor em tempo integral
    total_learners = models.IntegerField()  # Total de alunos do instrutor

    def __str__(self):
        return self.user.username  # Retorna o nome de usuário como representação textual

# Modelo para alunos/estudantes
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # Opções para a ocupação do aluno
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)  # Link para mídias sociais do aluno

    def __str__(self):
        return self.user.username + "," + self.occupation

# Modelo para cursos
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')  # Imagem associada ao curso
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)  # Data de publicação do curso
    instructors = models.ManyToManyField(Instructor)  # Relacionamento muitos-para-muitos com instrutores
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)  # Total de matrículas no curso
    is_enrolled = models.BooleanField(default=False)  # Indica se o usuário está matriculado no curso

    def __str__(self):
        return "Name: " + self.name + "," + "Description: " + self.description

# Modelo para lições
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)  # Ordem da lição no curso
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Relacionamento com o curso
    content = models.TextField()  # Conteúdo da lição

    def __str__(self):
        return "Titulo: " + self.title 
    
# Modelo para matrículas/enrollments
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)  # Data de matrícula
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)  # Modo da matrícula
    rating = models.FloatField(default=5.0)  # Avaliação da matrícula

# Modelo para perguntas/question
class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)  # Relacionamento com a lição
    question_text = models.TextField()  # Texto da pergunta
    question_grade = models.FloatField()  # Nota/pontuação da pergunta

    def is_get_score(self, selected_ids):
        # Método para verificar se o aluno obteve a pontuação na pergunta
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        else:
            return False

# Modelo para opções de escolha
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Relacionamento com a pergunta
    choice_text = models.CharField(max_length=200)  # Texto da opção de escolha
    is_correct = models.BooleanField(default=False)  # Indica se a opção é a correta

# Modelo para submissões/submissions
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)  # Relacionamento com a matrícula
    choices = models.ManyToManyField(Choice)  # Relacionamento muitos-para-muitos com as opções de escolha
    # Outros campos e métodos que você deseja projetar



class Pergunta(models.Model):
    texto_pergunta = models.CharField(max_length=200)

    def __str__(self):
        return self.texto_pergunta

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto_resposta = models.CharField(max_length=100)
    correta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto_resposta


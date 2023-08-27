from django.contrib import admin
from .models import Instructor, Learner, Course, Lesson, Enrollment, Question, Choice, Submission

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'lesson']
    
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'is_correct']

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)  # Register QuestionAdmin instead of Question
admin.site.register(Choice, ChoiceAdmin)      # Register ChoiceAdmin instead of Choice
admin.site.register(Submission)

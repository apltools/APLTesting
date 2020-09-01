from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django import forms
from testingapp.models import Question, Test
import basis_testing

class EntryView(View):
    def get(self, request, *args, **kwargs):
        # send token to relevant course site
        # TODO

        request.session['name'] = 'Placeholder'
        request.session['token'] = 'Placeholder'
        request.session['course_site'] = self.kwargs['site']

        return redirect('select')

class DoneView(View):
    def get(self, request, *args, **kwargs):
        # Prepare data we still need
        test = Test.objects.filter(short=request.session['test']).first()
        context = {
            'amount_correct': request.session['correct'],
            'amount_total': request.session['total'],
            'test': test.name
        }

        del request.session['correct']
        del request.session['total']
        del request.session['test']
        del request.session['question']
        del request.session['repeat']

        return render(request, 'testingapp/done.html', context)
        
class StartView(View):
    def get(self, request, *args, **kwargs):
        # send token to relevant course site
        # TODO

        request.session['test'] = self.kwargs['test']
        request.session['question'] = 1
        request.session['repeat'] = 1
        request.session['correct'] = 0
        request.session['total'] = 0

        return redirect('test')

class TestView(View):
    def get(self, request, *args, **kwargs):
        # Get the test and question
        test = Test.objects.filter(short=request.session['test']).first()
        question = Question.objects.filter(test=test, order=request.session['question']).first()
        
        if not question:
            return redirect('done')

        # Generate test if required
        if not 'answers' in request.session or not 'code' in request.session:
            template = basis_testing.Template(question.template, validator='basis')

            if question.question_type == 'Final value':
                template.complete().calc_end_values()
                request.session['answers'] = template.end_values
                request.session['code'] = template.full_test
            elif question.question_type == 'Evaluate':
                template.complete().calc_evaluate()
                request.session['answers'] = {'result': template.evaluate}
                request.session['code'] = template.full_test

        # Prepare the form
        form = forms.Form()
        for value in request.session['answers']:
            form.fields[value] = forms.CharField(label=value)

        # Render
        return render(request, 'testingapp/question.html', {'form': form, 'test': test, 'question': question, 'full_text': request.session['code']})
    
    def post(self, request, *args, **kwargs):
        # Get the test and question
        test = Test.objects.filter(short=request.session['test']).first()
        question = Question.objects.filter(test=test, order=request.session['question']).first()

        # Prepare the form
        form = forms.Form(request.POST)
        for value in request.session['answers']:
            form.fields[value] = forms.CharField(label=value)

        # Process the form
        if form.is_valid():
            incorrect = False
            student_answers = ''

            # Check for wrong answers
            for value in request.session['answers']:
                if value != 'result':
                    student_answers += value + ': ' + form.cleaned_data[value].strip() + '; '
                else:
                    student_answers += form.cleaned_data[value].strip() + '; '

                # Compile the student's answers
                if request.session['answers'][value].strip().lower() != form.cleaned_data[value].strip().lower():
                    incorrect = True

            # Compile correct ansers
            correct_answers = ''
            for var in request.session['answers']:
                if var != 'result':
                    correct_answers += var + ': ' + request.session['answers'][var] + '; '
                else:
                    correct_answers += request.session['answers'][var] + '; '

            # Prepare for the next one
            code = request.session['code']
            del request.session['code']
            del request.session['answers']
            request.session['total'] += 1

            # Check for end of question
            if question.repeat <= request.session['repeat']:
                request.session['repeat'] = 1
                request.session['question'] += 1
            else:
                request.session['repeat'] += 1

            # Keep score
            if not incorrect:
                request.session['correct'] += 1

            # Render!
            return render(request, 'testingapp/answer.html', {'test': test, 'code': code, 'question': question, 'incorrect': incorrect, 'correct_answers': correct_answers, 'student_answers': student_answers, 'amount_correct': request.session['correct'], 'amount_total': request.session['total']})

        else:
            return HttpResponse(status=500)

class SelectionView(ListView):
    # define view params
    template_name = 'testingapp/selection.html'
    model = Test

class HomeView(TemplateView):
    # define view params
    template_name = 'testingapp/home.html'

class QuestionsListView(LoginRequiredMixin, ListView):
    # define view params
    template_name = 'testingapp/questions.html'
    model = Question

# update a single test
class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    # must be an admin
    model = Question
    fields = ['test', 'order', 'template', 'question_type', 'question_override', 'final_value_variable', 'active']
    template_name = 'testingapp/question_update.html'

    # redirect to list after updating
    def get_success_url(self):
        return reverse('questions')
    
    def get_context_data(self, **kwargs):
        context = super(QuestionUpdateView, self).get_context_data(**kwargs)
        context['variants'] = []

        qst = Question.objects.get(pk=self.kwargs['pk'])

        template = basis_testing.Template(qst.template, validator = 'basis')
        template.discover().find_variants()
        
        i = 0
        for variant in template.variants:
            template.complete(choice_backlog=list(variant))
            variant_text = template.full_test
            context['variants'].append((i, ' - '.join(variant), variant_text))
            i += 1

        return context

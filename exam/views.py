from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question, Choice, UserAnswer, TestAttempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question, Choice, UserAnswer, TestAttempt
from django.contrib import messages
def test_list(request):
    tests = Test.objects.all()
    if request.user.is_authenticated:
        user_attempts = TestAttempt.objects.filter(user=request.user).order_by('-timestamp')
    else:
        user_attempts = None
    context = {
        'tests': tests,
        'user_attempts': user_attempts
    }
    return render(request, 'exam/test_list.html', context)


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.all()
    
    # Initialize dictionaries to store answers
    answered_choices = {}
    answered_texts = {}
    unanswered_questions = []

    if request.method == 'POST':
        for question in questions:
            if question.question_type == 'MC':
                choice_id = request.POST.get(f'question_{question.id}')
                if choice_id:
                    answered_choices[question.id] = int(choice_id)
            elif question.question_type == 'WA':
                written_answer = request.POST.get(f'question_{question.id}')
                if written_answer:
                    answered_texts[question.id] = written_answer
        
        # Check if all questions are answered
        all_answered = True
        for question in questions:
            if question.question_type == 'MC' and question.id not in answered_choices:
                all_answered = False
                unanswered_questions.append(question.id)
            elif question.question_type == 'WA' and question.id not in answered_texts:
                all_answered = False
                unanswered_questions.append(question.id)

        if all_answered:
            # Create the test attempt and user answers
            test_attempt = TestAttempt.objects.create(user=request.user, test=test)
            for question in questions:
                if question.question_type == 'MC':
                    choice = Choice.objects.get(pk=answered_choices[question.id])
                    UserAnswer.objects.create(
                        user=request.user,
                        question=question,
                        selected_choice=choice,
                        test_attempt=test_attempt
                    )
                elif question.question_type == 'WA':
                    UserAnswer.objects.create(
                        user=request.user,
                        question=question,
                        written_answer=answered_texts[question.id],
                        test_attempt=test_attempt
                    )
            
            # Check if user wants to save the results
            save_results = request.POST.get('save_results') == 'yes'
            if save_results:
                return redirect('test_results', test_id=test_id, attempt_id=test_attempt.id)
            else:
                # If not saving, delete the attempt and answers
                test_attempt.delete()
                messages.info(request, 'Your results were not saved.')
                return redirect('test_list')
        else:
            messages.error(request, 'Please answer all the questions.')

    return render(request, 'exam/take_test.html', {
        'test': test,
        'questions': questions,
        'answered_choices': answered_choices,
        'answered_texts': answered_texts,
        'unanswered_questions': unanswered_questions
    })

@login_required
def submit_test(request, test_id):
    if request.method == 'POST':
        test = get_object_or_404(Test, pk=test_id)
        test_attempt = TestAttempt.objects.create(user=request.user, test=test)
        unanswered_questions = []
        answered_choices = {}
        answered_texts = {}

        for question in test.question_set.all():
            if question.question_type == 'MC':
                choice_id = request.POST.get(f'question_{question.id}')
                if choice_id:
                    choice = Choice.objects.get(pk=choice_id)
                    answered_choices[question.id] = choice_id
                    UserAnswer.objects.create(
                        user=request.user,
                        question=question,
                        selected_choice=choice,
                        test_attempt=test_attempt
                    )
                else:
                    unanswered_questions.append(question.id)
            elif question.question_type == 'WA':
                written_answer = request.POST.get(f'question_{question.id}')
                if written_answer:
                    answered_texts[question.id] = written_answer
                    UserAnswer.objects.create(
                        user=request.user,
                        question=question,
                        written_answer=written_answer,
                        test_attempt=test_attempt
                    )
                else:
                    unanswered_questions.append(question.id)

        if unanswered_questions:
            messages.error(request, 'Please answer all the questions.')
            return render(request, 'exam/take_test.html', {
                'test': test,
                'questions': test.question_set.all(),
                'unanswered_questions': unanswered_questions,
                'answered_choices': answered_choices,
                'answered_texts': answered_texts,
            })

        return redirect('test_results', test_id=test_id, attempt_id=test_attempt.id)
@login_required
def test_results(request, test_id, attempt_id):
    test = get_object_or_404(Test, pk=test_id)
    test_attempt = get_object_or_404(TestAttempt, pk=attempt_id, user=request.user)
    user_answers = UserAnswer.objects.filter(test_attempt=test_attempt)
    
    results = []
    correct_answers = 0
    total_questions = test.question_set.count()

    for user_answer in user_answers:
        question = user_answer.question
        correct_choice = question.choice_set.filter(is_correct=True).first()
        correct_answer = correct_choice.choice_text if correct_choice else ''
        user_selected_answer = user_answer.selected_choice.choice_text if user_answer.selected_choice else user_answer.written_answer
        
        if question.question_type == 'MC':
            is_user_right = user_answer.selected_choice == correct_choice
        else:
            # For written answers, you might want to implement a separate grading system
            # For now, we'll consider them incorrect
            is_user_right = False
        
        if is_user_right:
            correct_answers += 1 

        results.append({
            'question': question,
            'user_answer': user_selected_answer,
            'correct_answer': correct_answer,
            'is_user_right': is_user_right
        })

    # Calculate and update the score
    test_attempt.score = (correct_answers / total_questions) * 100
    test_attempt.save()

    return render(request, 'exam/test_results.html', {
        'test': test,
        'results': results,
        'attempt': test_attempt,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
    })

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'exam/question_detail.html', {'question': question})
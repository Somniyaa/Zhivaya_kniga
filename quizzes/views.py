from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Quiz, Question, Answer, QuizResult

def quizzes_list(request):
    quizzes = Quiz.objects.all()
    completed_quizzes = []
    
    if request.user.is_authenticated:
        completed_quizzes = QuizResult.objects.filter(
            user=request.user
        ).values_list('quiz_id', flat=True)
    
    return render(request, 'quizzes/list.html', {
        'quizzes': quizzes,
        'completed_quizzes': list(completed_quizzes)
    })


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all().prefetch_related('answers')
    
    return render(request, 'quizzes/quiz.html', {
        'quiz': quiz,
        'questions': questions
    })


@csrf_exempt
@login_required
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        questions = quiz.questions.all()
        score = 0
        
        for question in questions:
            user_answer = answers.get(str(question.id))
            if user_answer:
                correct_answer = question.answers.filter(is_correct=True).first()
                if correct_answer and str(correct_answer.id) == user_answer:
                    score += 1
        
        total = questions.count()
        
        # Обновляем или создаем результат (для повторного прохождения)
        result, created = QuizResult.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={'score': score, 'total': total}
        )
        
        return JsonResponse({
            'success': True,
            'score': score,
            'total': total,
            'percentage': round(score / total * 100) if total > 0 else 0
        })
    
    return JsonResponse({'success': False}, status=400)
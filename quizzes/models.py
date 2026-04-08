from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField('Название', max_length=200)
    level = models.CharField('Уровень', max_length=100)
    description = models.TextField('Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'
    
    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField('Вопрос')
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f'{self.quiz.title} - {self.text[:50]}'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Ответ', max_length=200)
    is_correct = models.BooleanField('Правильный', default=False)
    
    def __str__(self):
        return self.text


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField('Количество правильных ответов')
    total = models.IntegerField('Всего вопросов')
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'quiz']
    
    def __str__(self):
        return f'{self.user.username} - {self.quiz.title}: {self.score}/{self.total}'
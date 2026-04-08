import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhivaya_kniga.settings')
django.setup()

from quizzes.models import Quiz, Question, Answer

def create_quizzes():
    # Викторина 1: Сказки Пушкина
    quiz1, created1 = Quiz.objects.get_or_create(
        title="Сказки Пушкина",
        defaults={
            'description': "Проверьте, как хорошо вы знаете сказки Александра Сергеевича Пушкина!"
        }
    )
    
    if created1:
        questions_data = [
            {'text': "Как звали царя в 'Сказке о золотом петушке'?", 'answers': [("Дадон", True), ("Гвидон", False), ("Салтан", False), ("Елисей", False)]},
            {'text': "Кого поймал старик в 'Сказке о рыбаке и рыбке'?", 'answers': [("Золотую рыбку", True), ("Щуку", False), ("Карася", False), ("Окуня", False)]},
            {'text': "Сколько раз закидывал старик невод в море?", 'answers': [("2", False), ("3", True), ("4", False), ("5", False)]},
            {'text': "Кем стала старуха в конце сказки о рыбаке и рыбке?", 'answers': [("Царицей", False), ("Столбовой дворянкой", False), ("У разбитого корыта", True), ("Владычицей морской", False)]},
            {'text': "Как звали царевну из 'Сказки о мёртвой царевне'?", 'answers': [("Золушка", False), ("Белоснежка", False), ("Спящая красавица", False), ("Царевна", True)]},
            {'text': "Кто дал царю Дадону золотого петушка?", 'answers': [("Звездочёт", True), ("Колдун", False), ("Чародей", False), ("Мудрец", False)]},
            {'text': "Что обещала золотая рыбка старику в обмен на свободу?", 'answers': [("Новое корыто", False), ("Дом", False), ("Исполнить три желания", False), ("Откуп", True)]},
            {'text': "В кого превращался князь Гвидон в 'Сказке о царе Салтане'?", 'answers': [("В муху, комара, шмеля", True), ("В сокола, орла, ястреба", False), ("В волка, медведя, лису", False), ("В лебедя, утку, гуся", False)]},
            {'text': "Сколько богатырей вышло из моря в 'Сказке о царе Салтане'?", 'answers': [("30", False), ("33", True), ("40", False), ("50", False)]},
            {'text': "Что попросила старуха у рыбки в первый раз?", 'answers': [("Новое корыто", True), ("Новую избу", False), ("Стать дворянкой", False), ("Стать царицей", False)]},
        ]
        
        for i, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(quiz=quiz1, text=q_data['text'], order=i)
            for answer_text, is_correct in q_data['answers']:
                Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
        
        print(f" Викторина '{quiz1.title}' создана с {len(questions_data)} вопросами")
    else:
        print(f" Викторина '{quiz1.title}' уже существует")

    # Викторина 2: Русские народные сказки
    quiz2, created2 = Quiz.objects.get_or_create(
        title="Русские народные сказки",
        defaults={
            'description': "Угадайте персонажей русских народных сказок!"
        }
    )
    
    if created2:
        questions_data = [
            {'text': "Кто жил в избушке на курьих ножках?", 'answers': [("Баба-Яга", True), ("Кощей Бессмертный", False), ("Леший", False), ("Водяной", False)]},
            {'text': "Кто сломал теремок?", 'answers': [("Медведь", True), ("Волк", False), ("Лиса", False), ("Заяц", False)]},
            {'text': "Как звали девочку, которая заблудилась в лесу и попала к медведям?", 'answers': [("Маша", True), ("Даша", False), ("Глаша", False), ("Наташа", False)]},
            {'text': "Кого обманула лиса, сказав, что она глухая?", 'answers': [("Волка", False), ("Медведя", False), ("Петуха", False), ("Кота", True)]},
            {'text': "Кто выгнал лису из заячьей избушки?", 'answers': [("Петух", True), ("Волк", False), ("Медведь", False), ("Собака", False)]},
            {'text': "Что несла Красная Шапочка бабушке?", 'answers': [("Пирожки и горшочек масла", True), ("Цветы", False), ("Книгу", False), ("Игрушки", False)]},
            {'text': "Кто помогал крошечке-Хаврошечке?", 'answers': [("Корова", True), ("Собака", False), ("Кошка", False), ("Птица", False)]},
            {'text': "Как звали мальчика, которого унесли гуси-лебеди?", 'answers': [("Иванушка", True), ("Алеша", False), ("Петя", False), ("Коля", False)]},
            {'text': "Из чего сварил кашу солдат в сказке 'Каша из топора'?", 'answers': [("Из топора", True), ("Из крупы", False), ("Из муки", False), ("Из гороха", False)]},
            {'text': "Кого в сказке 'Колобок' съел колобок последним?", 'answers': [("Лису", True), ("Зайца", False), ("Волка", False), ("Медведя", False)]},
        ]
        
        for i, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(quiz=quiz2, text=q_data['text'], order=i)
            for answer_text, is_correct in q_data['answers']:
                Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
        
        print(f" Викторина '{quiz2.title}' создана с {len(questions_data)} вопросами")
    else:
        print(f" Викторина '{quiz2.title}' уже существует")

    # Викторина 3: Детская литература
    quiz3, created3 = Quiz.objects.get_or_create(
        title="Детская литература",
        defaults={
            'description': "Вопросы о любимых детских книгах и их героях!"
        }
    )
    
    if created3:
        questions_data = [
            {'text': "Кто написал 'Приключения Тома Сойера'?", 'answers': [("Марк Твен", True), ("Чарльз Диккенс", False), ("Редьярд Киплинг", False), ("Джек Лондон", False)]},
            {'text': "Как звали девочку, которая попала в Страну чудес?", 'answers': [("Алиса", True), ("Венди", False), ("Дороти", False), ("Люси", False)]},
            {'text': "Кто был другом Маугли из 'Книги джунглей'?", 'answers': [("Багира", True), ("Шерхан", False), ("Акела", False), ("Каа", False)]},
            {'text': "Сколько оловянных солдатиков было в сказке Андерсена?", 'answers': [("24", False), ("25", True), ("30", False), ("12", False)]},
            {'text': "Как звали мальчика, который не хотел взрослеть?", 'answers': [("Питер Пэн", True), ("Том Сойер", False), ("Гарри Поттер", False), ("Мальчик-с-пальчик", False)]},
            {'text': "Кто автор книги 'Винни-Пух и все-все-все'?", 'answers': [("Алан Милн", True), ("Льюис Кэрролл", False), ("Джоан Роулинг", False), ("Астрид Линдгрен", False)]},
            {'text': "Как звали девочку, которая путешествовала по Изумрудному городу?", 'answers': [("Элли", True), ("Дороти", False), ("Анна", False), ("Мэри", False)]},
            {'text': "Кто написал 'Маленького принца'?", 'answers': [("Антуан де Сент-Экзюпери", True), ("Виктор Гюго", False), ("Оскар Уайльд", False), ("Эрнест Хемингуэй", False)]},
            {'text': "Как звали няню, которая летала с зонтиком?", 'answers': [("Мэри Поппинс", True), ("Фрекен Бок", False), ("Миссис Хадсон", False), ("Мисс Марпл", False)]},
            {'text': "Кто написал сказку 'Золотой ключик, или Приключения Буратино'?", 'answers': [("Алексей Толстой", True), ("Корней Чуковский", False), ("Самуил Маршак", False), ("Николай Носов", False)]},
        ]
        
        for i, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(quiz=quiz3, text=q_data['text'], order=i)
            for answer_text, is_correct in q_data['answers']:
                Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
        
        print(f" Викторина '{quiz3.title}' создана с {len(questions_data)} вопросами")
    else:
        print(f" Викторина '{quiz3.title}' уже существует")
    
    print("\n Готово!")

if __name__ == "__main__":
    create_quizzes()
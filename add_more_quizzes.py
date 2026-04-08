import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhivaya_kniga.settings')
django.setup()

from quizzes.models import Quiz, Question, Answer

def create_additional_quizzes():
    # Викторина 4: Зарубежные сказки
    quiz4, created4 = Quiz.objects.get_or_create(
        title="Зарубежные сказки",
        defaults={
            'description': "Проверьте свои знания о сказках народов мира!"
        }
    )
    
    if created4:
        questions_data = [
            {'text': "Кто написал сказку 'Красная Шапочка'?", 'answers': [("Шарль Перро", True), ("Братья Гримм", False), ("Ганс Христиан Андерсен", False), ("Вильгельм Гауф", False)]},
            {'text': "Как звали девочку, которая попала в Страну Оз?", 'answers': [("Дороти", True), ("Алиса", False), ("Венди", False), ("Элли", False)]},
            {'text': "Кто был лучшим другом Винни-Пуха?", 'answers': [("Пятачок", True), ("Кролик", False), ("Иа-Иа", False), ("Тигра", False)]},
            {'text': "Как звали принца, который поцеловал Спящую красавицу?", 'answers': [("Филипп", True), ("Шарман", False), ("Эрик", False), ("Генри", False)]},
            {'text': "Из чего был сделан Карлсон?", 'answers': [("Из пропеллера", True), ("Из металла", False), ("Из дерева", False), ("Из бумаги", False)]},
            {'text': "Кто подарил Золушке хрустальные туфельки?", 'answers': [("Фея-крёстная", True), ("Принц", False), ("Мачеха", False), ("Сёстры", False)]},
            {'text': "Как звали белого медвежонка из сказки?", 'answers': [("Умка", True), ("Бамси", False), ("Нуки", False), ("Ларс", False)]},
            {'text': "Кто написал 'Маленького Мука'?", 'answers': [("Вильгельм Гауф", True), ("Братья Гримм", False), ("Шарль Перро", False), ("Ганс Христиан Андерсен", False)]},
            {'text': "Как звали оленя из сказки о Снежной королеве?", 'answers': [("Олень", True), ("Рудольф", False), ("Бэмби", False), ("Свен", False)]},
            {'text': "Кто написал сказку 'Стойкий оловянный солдатик'?", 'answers': [("Ганс Христиан Андерсен", True), ("Шарль Перро", False), ("Братья Гримм", False), ("Вильгельм Гауф", False)]},
        ]
        
        for i, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(quiz=quiz4, text=q_data['text'], order=i)
            for answer_text, is_correct in q_data['answers']:
                Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
        
        print(f"✅ Викторина '{quiz4.title}' создана с {len(questions_data)} вопросами")
    else:
        print(f"⚠️ Викторина '{quiz4.title}' уже существует")

    # Викторина 5: Сказки Андерсена
    quiz5, created5 = Quiz.objects.get_or_create(
        title="Сказки Андерсена",
        defaults={
            'description': "Как хорошо вы знаете сказки великого датского сказочника?"
        }
    )
    
    if created5:
        questions_data = [
            {'text': "Как звали девочку, которая появилась из цветка?", 'answers': [("Дюймовочка", True), ("Эльза", False), ("Герда", False), ("Русалочка", False)]},
            {'text': "Во что превратился гадкий утёнок?", 'answers': [("В лебедя", True), ("В орла", False), ("В павлина", False), ("В журавля", False)]},
            {'text': "Кто украл снежную королеву?", 'answers': [("Кай", True), ("Герда", False), ("Снежная королева", False), ("Разбойница", False)]},
            {'text': "Что подарила русалочка ведьме в обмен на ноги?", 'answers': [("Свой голос", True), ("Свои волосы", False), ("Свое сердце", False), ("Свои глаза", False)]},
            {'text': "Сколько оловянных солдатиков было в коробке?", 'answers': [("25", True), ("24", False), ("30", False), ("20", False)]},
            {'text': "Что стало с маленькой русалочкой в конце сказки?", 'answers': [("Превратилась в морскую пену", True), ("Вышла замуж за принца", False), ("Вернулась в море", False), ("Стала королевой", False)]},
            {'text': "Кто помогал Герде искать Кая?", 'answers': [("Ворон", True), ("Олень", False), ("Цветы", False), ("Рыбы", False)]},
            {'text': "Из чего была сделана одежда короля в сказке 'Новое платье короля'?", 'answers': [("Из ничего", True), ("Из золота", False), ("Из шёлка", False), ("Из паутины", False)]},
            {'text': "Кто был принцессой на горошине?", 'answers': [("Настоящая принцесса", True), ("Королевна", False), ("Царевна", False), ("Герцогиня", False)]},
            {'text': "Что согревало Дюймовочку в норке полевой мыши?", 'answers': [("Ласточка", True), ("Крот", False), ("Цветы", False), ("Огонь", False)]},
        ]
        
        for i, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(quiz=quiz5, text=q_data['text'], order=i)
            for answer_text, is_correct in q_data['answers']:
                Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
        
        print(f"✅ Викторина '{quiz5.title}' создана с {len(questions_data)} вопросами")
    else:
        print(f"⚠️ Викторина '{quiz5.title}' уже существует")

    # Викторина 6: Сказки братьев Гримм
    quiz6, created6 = Quiz.objects.get_or_create(
        title="Сказки братьев Гримм",
        defaults={
            'description': "Вспомните любимые сказки братьев Гримм!"
        }
    )
    
    if created6:
        questions_data = [
            {'text': "Как звали девочку с длинными золотыми волосами?", 'answers': [("Рапунцель", True), ("Белоснежка", False), ("Златовласка", False), ("Золушка", False)]},
            {'text': "Что оставила Золушка на балу?", 'answers': [("Хрустальную туфельку", True), ("Перчатку", False), ("Платок", False), ("Кольцо", False)]},
            {'text': "Как звали семерых гномов?", 'answers': [("У каждого было имя", True), ("Белоснежка", False), ("Семь гномов", False), ("Имена не назывались", False)]},
            {'text': "Что случилось с принцем, который превратился в лягушку?", 'answers': [("Его поцеловала принцесса", True), ("Он съел волшебное яблоко", False), ("Он искупался в озере", False), ("Он разбил зеркало", False)]},
            {'text': "Как звали мальчика, который не мог перестать играть на дудочке?", 'answers': [("Крысолов", True), ("Гаммельн", False), ("Питер", False), ("Франц", False)]},
            {'text': "Что пряла королевна в сказке 'Спящая красавица'?", 'answers': [("Пряжу", True), ("Золото", False), ("Шерсть", False), ("Шёлк", False)]},
            {'text': "Кто помогал портному сшить платье для короля?", 'answers': [("Эльфы", True), ("Гномы", False), ("Феи", False), ("Мыши", False)]},
            {'text': "Что нашёл мельник в сказке 'Кот в сапогах'?", 'answers': [("Кота", True), ("Золото", False), ("Мешок", False), ("Замок", False)]},
            {'text': "Как звали девушку, которая жила в лесной избушке с медведями?", 'answers': [("Маша", True), ("Аленушка", False), ("Настенька", False), ("Катюша", False)]},
            {'text': "Что случилось с королём, который любил золото?", 'answers': [("Всё, к чему он прикасался, превращалось в золото", True), ("Он стал бедным", False), ("Он потерял королевство", False), ("Он стал невидимым", False)]},
        ]
        
        for i, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(quiz=quiz6, text=q_data['text'], order=i)
            for answer_text, is_correct in q_data['answers']:
                Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
        
        print(f"✅ Викторина '{quiz6.title}' создана с {len(questions_data)} вопросами")
    else:
        print(f"⚠️ Викторина '{quiz6.title}' уже существует")
    
    print("\n🎉 Все новые викторины успешно созданы!")

if __name__ == "__main__":
    create_additional_quizzes()
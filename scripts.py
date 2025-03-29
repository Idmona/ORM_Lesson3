import random
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation

PRAISE_TEXTS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!"
]


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject_title):
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__contains=subject_title
    ).order_by('-date').first()

    if not lesson:
        print("Ошибка: Урок не найден. Невозможно добавить похвалу.")
        return

    random_praise = random.choice(PRAISE_TEXTS)
    Commendation.objects.create(
        text=random_praise,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )


def main():
    schoolkid_full_name = "Фролов Иван"  # Укажите ФИО ученика здесь
    subject_title = "Математика"  # Укажите название предмета здесь

    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
        fix_marks(child)
        remove_chastisements(child)
        create_commendation(child, subject_title)

    except Schoolkid.DoesNotExist:
        print("Ошибка: Ученик не найден. Проверьте правильность ФИО ученика.")
        return
    except Schoolkid.MultipleObjectsReturned:
        print(f"Ошибка: Найдено несколько учеников с именем, содержащим '{schoolkid_full_name}'. Уточните ФИО.")
        return


if __name__ == "__main__":
    main()

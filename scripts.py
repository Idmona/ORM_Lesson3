import random
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid):
    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter
    ).order_by('-date').first()

    praise_texts = [
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

    random_praise = random.choice(praise_texts)

    Commendation.objects.create(
        text=random_praise,
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
    )


def main():
    schoolkid_full_name = "Фролов Иван"  # Укажите ФИО ученика здесь
    subject_title = "Математика"  # Укажите название предмета здесь

    try:

        child = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)

        lessons = Lesson.objects.filter(
            year_of_study=child.year_of_study,
            group_letter=child.group_letter,
            subject__title__contains=subject_title
        )

        if not lessons.exists():
            print(f"Ошибка: Убедитесь, что название предмета введено правильно.")
            return

        random_lesson = random.choice(list(lessons))

        fix_marks(child)

        remove_chastisements(child)

        create_commendation(child, random_lesson)



    except Schoolkid.DoesNotExist:
        print(f"Ошибка: Ученик не найден. Проверьте правильность ФИО ученика.")
        return
    except Schoolkid.MultipleObjectsReturned:
        print(f"Ошибка: Найдено несколько учеников с именем, содержащим '{schoolkid_full_name}'. Уточните ФИО.")
        return


if __name__ == "__main__":
    main()

import random
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    deleted_count = chastisements.delete()


def create_commendation(schoolkid, random_lesson):
    Commendation.objects.create(
        text="Молодец!", # Укажите текст похвалы
        created=random_lesson.date,
        schoolkid=schoolkid,
        subject=random_lesson.subject,
        teacher=random_lesson.teacher
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

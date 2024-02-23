from faker import Faker
from random import randint, choice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Teacher, Group, Student, Subject, Grade

# Создаем соединение с базой данных
engine = create_engine('postgresql://postgres:12345678@localhost:5432/hw2')
Base.metadata.bind = engine

# Создаем сессию
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Создаем объект Faker для генерации случайных данных
fake = Faker()

# Генерируем данные для групп
groups = [Group(name=f'Group {i}') for i in range(1, 4)]

# Генерируем данные для учителей
teachers = [Teacher(fullname=fake.name()) for _ in range(3)]

# Генерируем данные для предметов
subjects = [Subject(name=fake.word(), teacher=choice(teachers)) for _ in range(5)]

# Добавляем данные в сессию
session.add_all(groups)
session.add_all(teachers)
session.add_all(subjects)
session.commit()

# Генерируем данные для студентов
students = []
for _ in range(30):
    student = Student(fullname=fake.name(), group=choice(groups))
    students.append(student)

# Добавляем данные в сессию
session.add_all(students)
session.commit()

# Генерируем данные для оценок
for student in students:
    for subject in subjects:
        for _ in range(randint(1, 4)):
            grade = Grade(
                grade=randint(1, 12),
                grade_date=fake.date_between(start_date='-1y', end_date='today'),
                student_id=student.id,
                subject_id=subject.id  # Вот здесь исправление
            )
            session.add(grade)
        session.commit() # Добавляем коммит после каждого цикла оценок


print("Данные успешно добавлены в базу данных.")

import pytest

from django.contrib.auth.models import User

from projecttracker.models import Team, Employee, Project


@pytest.mark.django_db
def test_user_create():
    # given
    username = 'cmiranda'
    email = 'crism60@gmail.com'
    password = 'MyS3cr3tP455w0rD!#'
    previous_count = User.objects.count()

    # when
    user = User.objects.create_user(username=username, email=email, password=password)

    # then
    assert User.objects.count() == previous_count + 1
    assert User.objects.get(username=username) == user


@pytest.mark.django_db
def test_create_team():
    # given
    name = 'Equipo A'
    nick = 'A'
    description = 'Primer Equipo'
    employees = []
    for employee in ['Román', 'Oktavia', 'Jorge']:
        employees.append(Employee.objects.create(name=employee))
    

    # when
    team = Team.objects.create(name=name, nick=nick, description=description)
    team.employees.set(employees)

    # then
    assert Team.objects.get(name=name) == team


@pytest.mark.django_db
def test_create_employee():
    # given
    previous_employee_count = Employee.objects.count()
    employees = ['Cristian', 'Damián', 'Emmanuel']

    # when
    for employee in employees:
        Employee.objects.create(name=employee)

    # then
    assert Employee.objects.count() == previous_employee_count + len(employees)


@pytest.mark.django_db
def test_create_project():
    # given
    employees = []
    for employee in ['Román', 'Oktavia', 'Jorge']:
        employees.append(Employee.objects.create(name=employee))
    leader = employees[1]
    team = Team.objects.create(name='Equipo B', nick='B', description='Segundo equipo')
    team.employees.set(employees)

    # when
    project = Project.objects.create(team=team, leader=leader, datetime='2022-01-30 12:00:00', notes='')

    # then
    assert Project.objects.all().first() == project

import pytest
from django.urls import reverse

from projecttracker.models import Team, Employee, Project


@pytest.mark.django_db
def test_access_to_homepage(client):
    # given
    uri = reverse('home')

    # when
    response = client.get(uri)

    # then
    assert response.status_code == 200


@pytest.mark.django_db
def test_access_to_invalid_page(client):
    # given
    uri = 'this-page-doesnt-exist'

    # when
    response = client.get(uri)

    # then
    assert response.status_code == 404


@pytest.mark.django_db
def test_filter_by_team(client):
    # given
    team_name = 'Equipo-1'
    team = Team.objects.create(name=team_name, nick='T', description='')

    # when
    uri = reverse('home') + team_name
    response = client.get(uri)

    # then
    assert response.status_code == 200
    assert response.context['team_name'] == team_name
    assert response.context['filtered_team'] == team


@pytest.mark.django_db
def test_filter_by_invalid_team_name(client):
    # given
    team_name = 'Equipo Z'

    # when
    uri = reverse('home') + team_name
    response = client.get(uri)

    # then
    assert response.status_code == 200
    assert response.context['team_name'] == team_name
    assert response.context['error'] == f"Invalid team: {team_name}"


@pytest.mark.django_db
def test_show_team_projects(client):
    # given
    project, team, employees = create_project_bundle()

    # when
    uri = reverse('home') + team.name
    response = client.get(uri)

    # then
    assert response.status_code == 200
    assert response.context['team_name'] == team.name
    assert response.context['filtered_team'] == team
    assert response.context['projects'][0] == project
    assert response.context['amount_of_projects'] == len(response.context['projects'])
    assert len(response.context['employees']) == len(employees)


@pytest.mark.django_db
def test_show_all_projects(client):
    # given
    project, team, employees = create_project_bundle()

    # when
    uri = reverse('home')
    response = client.get(uri)

    # then
    assert response.status_code == 200
    assert response.context['team_name'] is None
    assert response.context['filtered_team'] is None
    assert response.context['projects'][0] == project
    assert response.context['amount_of_projects'] == len(response.context['projects'])


def create_project_bundle():
    employees = []
    for employee in ['Román', 'Oktavia', 'Jorge']:
        employees.append(Employee.objects.create(name=employee))
    leader = employees[1]
    team = Team.objects.create(name='Equipo B', nick='B', description='Segundo equipo')
    team.employees.set(employees)

    project = Project.objects.create(team=team, leader=leader, datetime='2022-01-30 12:00:00', notes='')

    return project, team, employees


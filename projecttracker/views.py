from django.shortcuts import render

from .models import *


def home(request, team_name=None):
    filtered_team = None
    context = {}

    context["team_name"] = team_name
    context["teams"] = Team.objects.all().order_by("name")

    if team_name:
        search = Team.objects.filter(name__iexact=team_name)
        if len(search) == 1:
            filtered_team = search.get()
        else:
            context["error"] = f"Invalid team: {team_name}"

            return render(request, "index.html", context)

        projects = Project.objects.filter(team=filtered_team).order_by("-datetime")
        context["filtered_team_employees"] = ', '.join(
            list(map(lambda employee: employee.name, filtered_team.employees.all()))
        )
    else:
        projects = Project.objects.all().order_by("-datetime")

    context["projects"] = projects
    context["employees"] = Employee.objects.all().order_by("name")
    context["filtered_team"] = filtered_team
    context["amount_of_projects"] = len(context["projects"])

    return render(request, "index.html", context)

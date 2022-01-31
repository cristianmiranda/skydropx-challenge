from django.db import models
from django.contrib import admin


class Employee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


admin.site.register(Employee)


class Team(models.Model):
    name = models.CharField(max_length=100)
    nick = models.CharField(max_length=5)
    description = models.TextField()
    employees = models.ManyToManyField(Employee, related_name="projects", verbose_name="List of employees")

    def __str__(self):
        return self.name


admin.site.register(Team)


class Project(models.Model):
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
    leader = models.ForeignKey(Employee, default=None, related_name="leading_projects", on_delete=models.RESTRICT)
    datetime = models.DateTimeField()
    notes = models.TextField(default=None)

    def __str__(self):
        return f"Project involving {self.team.name}"

    class Meta:
        verbose_name_plural = "projects"


admin.site.register(Project)

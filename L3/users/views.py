from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse


# Create your views here.


def year_archive(request: HttpRequest, year: int) -> HttpResponse:
    return HttpResponse(f'<h1>Year {year}</h1> <a href={reverse("year_archive", args=[year])}>Ссылка на саму себя</a>')

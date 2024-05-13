from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse


def index(request):
    id = 1
    return HttpResponse(id)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import *

from .forms import *


# Create your views here.


def home(request):
    return render(
        request,
        "finance/home.html",
        {"incomes": Income.objects.all(), "expenses": Expense.objects.all()},
    )


def addexpense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            cost = form.cleaned_data["cost"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            date = form.cleaned_data["date"]
            expense = Expense(
                cost=cost, description=description, category=category, date=date
            )
            expense.save()
            return redirect("home")
    else:
        form = ExpenseForm()

    return render(request, "finance/add.html", {"form": form, "type": "expense"})


def addincome(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            cost = form.cleaned_data["cost"]
            source = form.cleaned_data["source"]
            description = form.cleaned_data["description"]
            date = form.cleaned_data["date"]
            expense = Income(
                cost=cost, description=description, source=source, date=date
            )
            expense.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        form = IncomeForm()

    return render(request, "finance/add.html", {"form": form, "type": "income"})


def updateincome(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = IncomeForm(instance=income)
        return render(
            request,
            "finance/update.html",
            {
                "form": form,
                "type": "income",
                "income": Income.objects.get(id=income_id),
            },
        )


def updateexpense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ExpenseForm(instance=expense)
        return render(
            request,
            "finance/update.html",
            {
                "form": form,
                "type": "expense",
                "expense": Expense.objects.get(id=expense_id),
            },
        )


def deleteexpense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.method == "POST":
        expense.delete()
        messages.success(request, f"{expense.description} deleted")
        return redirect("home")
    return render(
        request, "finance/delete.html", {"expense": expense, "type": "expense"}
    )


def deleteincome(request, income_id):
    income = Income.objects.get(id=income_id)
    if request.method == "POST":
        income.delete()
        messages.success(request, f"{income.description} deleted")
        return redirect("home")
    return render(request, "finance/delete.html", {"income": income, "type": "income"})


# def addcategory(request):
#     if request.method == "POST":
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             category = form.cleaned_data["category"]
#             category = category.objects.get_or_create(name=category)
#             cat = Category(name = Category)
#             form.save()
#             return redirect("add")
#     else:
#         form = CategoryForm()
#     return render(
#         request, "finance/add_category.html", {"form": form, "type": "category"}
#     )

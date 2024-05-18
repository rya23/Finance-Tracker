from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from .models import *
from calendar import month_name
from .forms import *
from itertools import zip_longest

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

from plotly.offline import plot
from plotly.graph_objs import Bar


def report(request):
    expenses_by_month = (
        Expense.objects.annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(total_cost=Sum("cost"))
        .order_by("month")
    )
    incomes_by_month = (
        Income.objects.annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(total_cost=Sum("cost"))
        .order_by("month")
    )
    monthly_reports = []
    x = []
    y_expenses = []
    y_incomes = []
    for exp, inc in zip(expenses_by_month, incomes_by_month):
        month = month_name[exp["month"]]
        total_expense = exp["total_cost"] or 0
        total_income = inc["total_cost"] or 0
        difference = total_income - total_expense
        monthly_reports.append(
            {
                "month_name": month,
                "month_no": exp["month"],
                "total_expense": total_expense,
                "total_income": total_income,
                "difference": difference,
            }
        )
        x.append(month)
        y_expenses.append(total_expense)
        y_incomes.append(total_income)

    plot_div = plot(
        [
            Bar(
                x=x,
                y=y_expenses,
                name="Expenses",
                marker_color="red",
            ),
            Bar(
                x=x,
                y=y_incomes,
                name="Incomes",
                marker_color="blue",
            ),
        ],
        output_type="div",
    )

    return render(
        request,
        "finance/report.html",
        {"monthly_reports": monthly_reports, "plot_div": plot_div},
    )


# Call the function to generate the report


def month(request, month_no):
    incomes = Income.objects.filter(date__month=month_no)
    expenses = Expense.objects.filter(date__month=month_no)

    totalinc = incomes.aggregate(total_cost=Sum("cost"))["total_cost"]

    totalexp = expenses.aggregate(total_cost=Sum("cost"))["total_cost"]

    saving = totalinc - totalexp
    return render(
        request,
        "finance/month.html",
        {
            "incomes": incomes,
            "expenses": expenses,
            "totalinc": totalinc,
            "totalexp": totalexp,
            "saving": saving,
        },
    )

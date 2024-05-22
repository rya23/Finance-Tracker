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
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
from plotly.graph_objs import Bar, Pie

# Create your views here.


@login_required
def home(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    return render(
        request, "finance/home.html", {"incomes": incomes, "expenses": expenses}
    )


@login_required
def addexpense(request):
    if request.method == "POST":
        form = ExpenseForm(request.user, request.POST)
        if form.is_valid():
            cost = form.cleaned_data["cost"]
            category = form.cleaned_data["category"]

            if category.budget:
                total_expenses = Expense.objects.filter(category=category).aggregate(
                    total_cost=Sum("cost")
                )["total_cost"]
                if total_expenses + cost > category.budget:
                    messages.warning(
                        request, f"Budget Exceeded for {category.name} category."
                    )
            description = form.cleaned_data["description"]
            date = form.cleaned_data["date"]
            user = request.user
            expense = Expense(
                cost=cost,
                description=description,
                category=category,
                date=date,
                user=user,
            )
            expense.save()
            return redirect("home")
    else:
        form = ExpenseForm(user=request.user)

    return render(request, "finance/add.html", {"form": form, "type": "expense"})


@login_required
def addincome(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            cost = form.cleaned_data["cost"]
            source = form.cleaned_data["source"]
            description = form.cleaned_data["description"]
            date = form.cleaned_data["date"]
            user = request.user
            expense = Income(
                cost=cost,
                description=description,
                source=source,
                date=date,
                user=user,
            )
            expense.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        form = IncomeForm()

    return render(request, "finance/add.html", {"form": form, "type": "income"})


@login_required
def updateincome(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    if request.user == income.user:
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
    else:
        return redirect(home)


@login_required
def updateexpense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.user == expense.user:
        if request.method == "POST":
            form = ExpenseForm(request.user, request.POST, instance=expense)
            if form.is_valid():
                form.save()
                return redirect("home")
        else:
            form = ExpenseForm(user=request.user, instance=expense)
            return render(
                request,
                "finance/update.html",
                {
                    "form": form,
                    "type": "expense",
                    "expense": Expense.objects.get(id=expense_id),
                },
            )
    else:
        return redirect("home")


@login_required
def deleteexpense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.user == expense.user:
        if request.method == "POST":
            expense.delete()
            messages.success(request, f"{expense.description} deleted")
            return redirect("home")
        return render(
            request, "finance/delete.html", {"expense": expense, "type": "expense"}
        )
    else:
        return redirect("home")


@login_required
def deleteincome(request, income_id):
    income = Income.objects.get(id=income_id)
    if request.user == income.user:
        if request.method == "POST":
            income.delete()
            messages.success(request, f"{income.description} deleted")
            return redirect("home")
        return render(
            request, "finance/delete.html", {"income": income, "type": "income"}
        )
    else:
        return redirect("home")


def addcategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data["name"]
            user = request.user
            category, created = Category.objects.get_or_create(name=category_name)
            category.user = user
            category.save()
            return redirect("addexpense")
    else:
        form = CategoryForm()
    return render(
        request, "finance/add_category.html", {"form": form, "type": "category"}
    )


def addsource(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data["name"]
            source = Source.objects.get_or_create(name=source)
            Source(name=source)
            return redirect("addincome")
    else:
        form = CategoryForm()
    return render(
        request, "finance/add_category.html", {"form": form, "type": "source"}
    )


import calendar
from datetime import datetime


@login_required
def report(request):
    user = request.user
    expenses_by_month = (
        Expense.objects.filter(user=request.user)
        .annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(total_cost=Sum("cost"))
        .order_by("month")
    )
    incomes_by_month = (
        Income.objects.filter(user=request.user)
        .annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(total_cost=Sum("cost"))
        .order_by("month")
    )
    current_year = datetime.now().year

    # Initialize lists for storing data
    monthly_reports = []
    x = []
    y_expenses = []
    y_incomes = []

    # Loop through all months of the year
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        # Check if there are expenses for this month
        expenses = Expense.objects.filter(
            user=request.user, date__year=current_year, date__month=month
        ).aggregate(total_cost=Sum("cost"))
        total_expense = (
            expenses["total_cost"] if expenses["total_cost"] is not None else 0
        )
        # Check if there are incomes for this month
        incomes = Income.objects.filter(
            user=request.user, date__year=current_year, date__month=month
        ).aggregate(total_cost=Sum("cost"))
        total_income = incomes["total_cost"] if incomes["total_cost"] is not None else 0

        difference = total_income - total_expense

        # Append data to respective lists
        monthly_reports.append(
            {
                "month_name": month_name,
                "month_no": month,
                "total_expense": total_expense,
                "total_income": total_income,
                "difference": difference,
            }
        )
        x.append(month_name)
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
                marker_color="green",
            ),
        ],
        output_type="div",
    )

    expenses_by_category = (
        Expense.objects.filter(user=user)
        .values("category__name")
        .annotate(total_cost=Sum("cost"))
        .order_by("-total_cost")
    )
    incomes_by_source = (
        Income.objects.filter(user=user)
        .values("source__name")
        .annotate(total_cost=Sum("cost"))
        .order_by("-total_cost")
    )

    expense_labels = [expense["category__name"] for expense in expenses_by_category]
    expense_values = [expense["total_cost"] for expense in expenses_by_category]

    income_labels = [income["source__name"] for income in incomes_by_source]
    income_values = [income["total_cost"] for income in incomes_by_source]

    expense_pie = Pie(labels=expense_labels, values=expense_values, name="Expenses")
    income_pie = Pie(labels=income_labels, values=income_values, name="Incomes")

    expense_plot = plot([expense_pie], output_type="div")
    income_plot = plot([income_pie], output_type="div")

    return render(
        request,
        "finance/report.html",
        {
            "expense_plot": expense_plot,
            "income_plot": income_plot,
            "monthly_reports": monthly_reports,
            "plot_div": plot_div,
        },
    )


# Call the function to generate the report


@login_required
def month(request, month_no):
    incomes = Income.objects.filter(date__month=month_no, user=request.user)
    expenses = Expense.objects.filter(date__month=month_no, user=request.user)

    totalinc = incomes.aggregate(total_cost=Sum("cost"))["total_cost"] or 0

    totalexp = expenses.aggregate(total_cost=Sum("cost"))["total_cost"] or 0

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


@login_required
def addbudget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            category_name = form.cleaned_data["category"]
            budget = form.cleaned_data["budget"]
            category = Category.objects.get(name=category_name)
            category.budget = budget
            category.save()
            return redirect("home")
    else:
        form = BudgetForm(user=request.user)

    return render(request, "finance/addbudget.html", {"form": form})


# @login_required
# def deletebudget(request, category_id):
#     category = category.objects.get(id=expense_id)
#     if request.user == expense.user:
#         if request.method == "POST":
#             category.budget = NULL
#             messages.success(f"Budget of {category.name} deleted")
#             return redirect("home")
#         return render(
#             request, "finance/delete.html", {"category": category, "type": "category"}
#         )
#     else:
#         return redirect("home")


def category(request):
    user = request.user
    expenses_by_category = (
        Expense.objects.filter(user=user)
        .values("category__name")
        .annotate(total_cost=Sum("cost"))
        .annotate(budget=models.F("category__budget"))
        .order_by("-total_cost")
    )

    expense_labels = [expense["category__name"] for expense in expenses_by_category]
    expense_values = [expense["total_cost"] for expense in expenses_by_category]

    expense_pie = Pie(labels=expense_labels, values=expense_values, name="Expenses")

    expense_plot = plot([expense_pie], output_type="div")

    return render(
        request,
        "finance/category.html",
        {
            "expenses": expenses_by_category,
            "expense_plot": expense_plot,
        },
    )

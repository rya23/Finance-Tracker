from django import forms
from django.forms.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
from .models import *
from django.forms.fields import DateField


# class DateInput(forms.DateInput):
#     input_type = "date"


# class BaseTransactionForm(forms.Form):
#     date = forms.DateField(widget=DateInput, label="Date", required=True)
#     cost = forms.IntegerField(label="Cost")
#     description = forms.CharField(label="Description", max_length=200, required=False)


# class ExpenseForm(BaseTransactionForm):
#     category = forms.ModelChoiceField(
#         queryset=Category.objects.all(),
#         widget=forms.Select(attrs={"class": "select2"}),
#         required=False,
#     )


# class IncomeForm(BaseTransactionForm):
#     source = forms.ModelChoiceField(
#         queryset=Source.objects.all(),
#         widget=forms.Select(attrs={"class": "select2"}),
#         required=False,
#     )


class DateInput(forms.DateInput):
    input_type = "date"


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "cost", "category", "description"]
        widgets = {
            "date": DateInput(),
            "category": forms.Select(attrs={"class": "select2"}),
        }
        labels = {
            "date": "Date",
            "cost": "Cost",
            "description": "Description",
            "category": "Category",
        }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["date", "cost", "source", "description"]
        widgets = {
            "date": DateInput(),
            "source": forms.Select(attrs={"class": "select2"}),
        }
        labels = {
            "date": "Date",
            "cost": "Cost",
            "description": "Description",
            "source": "Source",
        }


# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ["name"]

from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("addexpense", views.addexpense, name="addexpense"),
    path("addincome", views.addincome, name="addincome"),
    # path("addcategory", views.addcategory, name="addcategory"),
    path("updateincome/<int:income_id>", views.updateincome, name="updateincome"),
    path("updateexpense/<int:expense_id>", views.updateexpense, name="updateexpense"),
    path("deleteexpense/<int:expense_id>", views.deleteexpense, name="deleteexpense"),
    path("deleteincome/<int:income_id>", views.deleteincome, name="deleteincome"),
    path("report", views.report, name="report"),
    path("month/<int:month_no>", views.month, name="month"),
]

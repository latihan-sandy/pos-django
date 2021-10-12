import random
import uuid 

from django import template
from transactions.models import TransactionDetail
from re import search


register = template.Library()

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)

@register.simple_tag
def random_uuid():
    return uuid.uuid1()

@register.inclusion_tag("app/reports/details.html")
def detail_transaction(transaction):
    listData = TransactionDetail.objects.filter(transaction = transaction)
    return { "data" : listData}


@register.simple_tag
def route_active(url, prefix):
    master = ("brands","categories", "customers","products","suppliers","types","groups","users")
    arr = url.split("/")

    if prefix == "master":
        if arr[1] in master:
            return "active"

    if prefix == "transaction":
        if arr[1]  == "transaction":
            return "active"

    if prefix == "account":
        if arr[1] == "account":
            return "active"

    return ""

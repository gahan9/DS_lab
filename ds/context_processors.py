# coding=utf-8
__author__ = "Gahan Saraiya"
from DBS_LAB.settings import COMPANY_TITLE


def site_details(request):
    return {
        "COMPANY_TITLE": COMPANY_TITLE,
    }

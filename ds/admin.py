from django.contrib import admin

from DBS_LAB.settings import COMPANY_TITLE
from ds.models import LeaderBoard, ProgrammingLanguage


@admin.register(LeaderBoard)
class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "language", "score", "organizer", "time", "country"]


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "version", "release"]


admin.site.site_header = COMPANY_TITLE + ' administration'
admin.site.site_title = COMPANY_TITLE + ' administration'
admin.site.index_title = COMPANY_TITLE + ' administration'

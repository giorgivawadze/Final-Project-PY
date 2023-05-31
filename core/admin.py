from django.contrib import admin

from core.models import Question, Choice, Tag

admin.site.register([Tag])

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1
    fields = ['text', 'votes']
    readonly_fields = ['votes']

@admin.register(Question)
class QuestionAdminModel(admin.ModelAdmin):
    inlines = [ChoiceInline]
    filter_horizontal = ['tags']
    list_display = ['title', 'create_time']
    search_fields = ['title', 'choice__text']
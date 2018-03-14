from django.contrib import admin
from models import *

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    # fields = ('title','desc','content',)
    # exclude =
    # fieldsets =
    # list_display =
    # list_display_links =
    # list_editable =
    # list_filter =
    # inlines =
    class Media:
        js = (
            'js/kindeditor-4.1.10/kindeditor-min.js',
            'js/kindeditor-4.1.10/lang/zh_CN.js',
            'js/kindeditor-4.1.10/config.js',
        )


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
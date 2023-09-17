# from django import forms
# from django.contrib import admin
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from ckeditor.widgets import CKEditorWidget

# from .models import CourseCategoriesModel, CourseModel, CourseCommentModel

# # Register your models here.


# class CourseCategoriesAdmin(admin.ModelAdmin):
#     list_display = ("image_icon_tag", "name", "slug")
#     fields = ("image_tag", "name", "photo", "slug")
#     readonly_fields = ("image_tag", )
#     search_fields = ("name", )
#     prepopulated_fields = {"slug": ("name", )}


# class CourseAdminForm(forms.ModelForm):
#     course_content = forms.CharField(widget=CKEditorUploadingWidget(config_name='uploader'))
#     course_more = forms.CharField(widget=CKEditorWidget(), required=False)

#     class Meta:
#         model = CourseModel
#         fields = "__all__"


# class CourseAdmin(admin.ModelAdmin):
#     list_display = ("category", "course_name", "author", "likes", "is_private","datetime_upload")
#     readonly_fields = ("image_tag", "datetime_upload")
#     search_fields = ("category", "course_name", "author", "course_author", "course_download_link", "datetime_upload")
#     prepopulated_fields = {"slug": ("course_author", "course_name")}
#     form = CourseAdminForm


# class CourseCommentsAdminForm(forms.ModelForm):
#     text = forms.CharField(widget=CKEditorUploadingWidget(config_name='uploader'))
#     class Meta:
#         model = CourseCommentModel
#         fields = "__all__"


# class CourseCommentsAdmin(admin.ModelAdmin):
#     list_display = ("text", "course")
#     readonly_fields = ("date_upload", )
#     search_fields = ("text", "course")
#     form = CourseCommentsAdminForm


# admin.site.register(CourseCategoriesModel, CourseCategoriesAdmin)
# admin.site.register(CourseModel, CourseAdmin)
# admin.site.register(CourseCommentModel, CourseCommentsAdmin)

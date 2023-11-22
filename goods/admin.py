from django import forms
from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget

from goods.widgets import CustomAdminFileWidget

from .models import ShoesModel, ShoesPhotoModel, JacketModel, JacketPhotoModel, TrouserModel, TrouserPhotoModel,  ThermalUnderwearModel, ThermalUnderwearPhotoModel, JumperModel, JumperPhotoModel, Technology, BrandModel

# Register your models here.

class TechnologyModelAdmin(admin.ModelAdmin):
    pass


class BrandModelAdmin(admin.ModelAdmin):
    pass


class CKFormMixin(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorWidget())

    class Meta:
        model = None
        fields = '__all__'


class ShoesCKForm(CKFormMixin):
    class Meta(CKFormMixin.Meta):
        model = ShoesModel


class JacketCKForm(CKFormMixin):
    class Meta(CKFormMixin.Meta):
        model = JacketModel

class TrouserCKForm(CKFormMixin):
    class Meta(CKFormMixin.Meta):
        model = TrouserModel

class ThermalUnderwearCKForm(CKFormMixin):
    class Meta(CKFormMixin.Meta):
        model = ThermalUnderwearModel

class JumperCKForm(CKFormMixin):
    class Meta(CKFormMixin.Meta):
        model = JumperModel


class ShoesPhotoStackedInline(admin.StackedInline):
    model = ShoesPhotoModel
    extra = 1
    classes = ('collapse', )
    
    formfield_overrides = {
        models.ImageField: {"widget": CustomAdminFileWidget}
    }

class ShoesModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('technologies', )
    form = ShoesCKForm
    fieldsets = (
        ('228', {
            'fields': ('title', 'price', 'description')
        }),
        ('Конструктивные особенности', {
            'fields': ('insulation_weight', 'clasp', 'reinforced_bumper' )
        }),
        ('Функциональные особенности', {
            'fields': ('antibacterial_impregnation', 'moisture_protection')
        }),
        ('Общие характеристики', {
            'fields': ('gender', 'age_type', 'sport_type', 'season', 'guarantee_period', 'product_authenticity_guarantee')
        }),
        ('Состав', {
            'fields': ('upper_material', 'lining_material', 'outsole_material', 'insole_material')
        }),
        ('Дополнительные характеристики', {
            'fields': ('brand', 'technologies')
        }),
    )
    search_fields = ('title', )
    inlines = (ShoesPhotoStackedInline, )


class ShoesPhotoModelAdmin(admin.ModelAdmin):
    list_display = ('image_tag', '__str__')
    fields = ('photo', 'shoes', 'image_tag')
    readonly_fields = ('image_tag', )

class JacketPhotoStackedInline(admin.StackedInline):
    model = JacketPhotoModel
    extra = 1
    classes = ('collapse', )
    
    formfield_overrides = {
        models.ImageField: {"widget": CustomAdminFileWidget}
    }
class JacketModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('technologies', )
    form = JacketCKForm
    fieldsets = (
        ('228', {
            'fields': ('title', 'price', 'description')
        }),
        ('Размер на модели', {
            'fields': ('model_parameters','product_size_on_model')
        }),
        ('Конструктивные особенности', {
            'fields': ('cut', 'possibility_of_packaging', 'length', 'ergonomic_cut', 'hood', 'сlasp', 
                       'taped_seams', 'number_of_pockets' ,'thumb_hole_in_cuff', 'cuff_adjustment', 'fur')
        }),
        ('Функциональные особенности', {
            'fields': ('presence_of_membrane', 'water_repellent_impregnation', 'waterproof_zippers', 'wind_protection','insulation')
        }),
        ('Общие характеристики', {
            'fields': ('gender', 'age_type', 'sport_type', 'season', 'guarantee_period', 'product_authenticity_guarantee')
        }),
        ('Состав', {
            'fields': ('upper_material', 'lining_material','insole_material')
        }),
        ('Дополнительные характеристики', {
            'fields': ('brand', 'technologies','reflective_details')
        }),
        ('Уход за товаром', {
            'fields': ('care_instructions', 'additional_information')
        }),
        
    )

    search_fields = ('title', )
    inlines = (JacketPhotoStackedInline, )
    
class JacketPhotoModelAdmin(admin.ModelAdmin):
    list_display = ('image_tag', '__str__')
    fields = ('photo', 'jacket', 'image_tag')
    readonly_fields = ('image_tag', )

class TrouserPhotoStackedInline(admin.StackedInline):
        model = TrouserPhotoModel
        extra = 1
        classes = ('collapse', )
    
formfield_overrides = {
        models.ImageField: {"widget": CustomAdminFileWidget}
    }

class TrouserModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('technologies', )
    form = TrouserCKForm
    fieldsets = (
        ('228', {
            'fields': ('title', 'price', 'description')
        }),
        ('Конструктивные особенности', {
            'fields': ('cut', 'possibility_of_packaging', 'length', 'ergonomic_cut', 'hood', 'сlasp', 
                       'taped_seams', 'number_of_pockets' ,'thumb_hole_in_cuff', 'cuff_adjustment', 'fur')
        }),
        ('Функциональные особенности', {
            'fields': ('presence_of_membrane', 'water_repellent_impregnation', 'waterproof_zippers', 'wind_protection','insulation')
        }),
        ('Общие характеристики', {
            'fields': ('gender', 'age_type', 'sport_type', 'season', 'guarantee_period', 'product_authenticity_guarantee')
        }),
        ('Состав', {
            'fields': ('upper_material', 'lining_material','insole_material')
        }),
        ('Дополнительные характеристики', {
            'fields': ('brand', 'technologies','reflective_details')
        }),
        ('Уход за товаром', {
            'fields': ('care_instructions', 'additional_information')
        }),
    )
    search_fields = ('title', )
    inlines = (TrouserPhotoStackedInline, )

class TrouserPhotoModelAdmin(admin.ModelAdmin):
    list_display = ('image_tag', '__str__')
    fields = ('photo', 'trousers', 'image_tag')
    readonly_fields = ('image_tag', )


class ThermalUnderwearPhotoStackedInline(admin.StackedInline):
        model = ThermalUnderwearPhotoModel
        extra = 1
        classes = ('collapse', )
    
formfield_overrides = {
        models.ImageField: {"widget": CustomAdminFileWidget}
    }

class ThermalUnderwearModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('technologies', )
    form = ThermalUnderwearCKForm
    fieldsets = (
        ('228', {
            'fields': ('title', 'price', 'description')
        }),
        ('Размер на модели', {
            'fields': ('model_parameters','product_size_on_model')
        }),
        ('Конструктивные особенности', {
            'fields': ('сut', 'length', 'flat_seams')
        }),
        ('Общие характеристики', {
            'fields': ('gender', 'age_type', 'sport_type','product_authenticity_guarantee')
        }),
        ('Дополнительные характеристики', {
            'fields': ('brand', 'technologies','materials')
        }),
        ('Уход за товаром', {
            'fields': ('care_instructions',)
        }),
    )
    search_fields = ('title', )
    inlines = (ThermalUnderwearPhotoStackedInline, )

class ThermalUnderwearPhotoModelAdmin(admin.ModelAdmin):
    list_display = ('image_tag', '__str__')
    fields = ('photo', 'thermal_underwear', 'image_tag')
    readonly_fields = ('image_tag', )


class JumperPhotoStackedInline(admin.StackedInline):
        model = JumperPhotoModel
        extra = 1
        classes = ('collapse', )
    
formfield_overrides = {
        models.ImageField: {"widget": CustomAdminFileWidget}
    }

class JumperModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('technologies', )
    form = JumperCKForm
    fieldsets = (
        ('228', {
            'fields': ('title', 'price', 'description')
        }),
        ('Размер на модели', {
            'fields': ('model_parameters','product_size_on_model')
        }),
        ('Конструктивные особенности', {
            'fields': ('сut', 'length', 'the_length_of_the_sleeve', 'clasp','number_of_pockets')
        }),
        ('Общие характеристики', {
            'fields': ('gender', 'age_type', 'season', 'product_authenticity_guarantee')
        }),
        ('Состав', {
            'fields': ('upper_material','lining_material', 'insole_material')
        }),
        ('Дополнительные характеристики', {
            'fields': ('brand', 'technologies')
        }),
         ('Уход за товаром', {
            'fields': ('care_instructions',)
        }),
    )

    search_fields = ('title', )
    inlines = (JumperPhotoStackedInline, )

class JumperPhotoModelAdmin(admin.ModelAdmin):
    list_display = ('image_tag', '__str__')
    fields = ('photo', 'jumper', 'image_tag')
    readonly_fields = ('image_tag', )


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

admin.site.register(Technology, TechnologyModelAdmin)
admin.site.register(BrandModel, BrandModelAdmin)

admin.site.register(ShoesModel, ShoesModelAdmin)
admin.site.register(ShoesPhotoModel, ShoesPhotoModelAdmin)

admin.site.register(JacketModel, JacketModelAdmin)
admin.site.register(JacketPhotoModel, JacketPhotoModelAdmin)

admin.site.register(TrouserModel, TrouserModelAdmin)
admin.site.register(TrouserPhotoModel, TrouserPhotoModelAdmin)

admin.site.register(ThermalUnderwearModel, ThermalUnderwearModelAdmin)
admin.site.register(ThermalUnderwearPhotoModel, ThermalUnderwearPhotoModelAdmin)

admin.site.register(JumperModel, JumperModelAdmin)
admin.site.register(JumperPhotoModel, JumperPhotoModelAdmin)

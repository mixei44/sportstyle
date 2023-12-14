from django.db import models
from django.utils.html import mark_safe

#БАЗА ДАННЫХ 

GENDER = [
    ('M', 'Мужской'),
    ('F', 'Женский'),
    ('B', 'Мальчик'),
    ('G', 'Девочка'),
]

AGE_TYPE = [
    ('L', 'Взрослые'),
    ('T', 'Подростки'),
    ('K', 'Дети'),
]

SPORT_TYPE = [
    ('H', 'Поход'),
    ('R', 'Бег'),
    ('F', 'Фитнес'),
    ('S', 'Лыжи'),
]

SEASON = [
    ('W', 'Зима'),
    ('S', 'Весна'),
    ('S', 'Лето'),
    ('A', 'Осень'),
]


class PhotoMixin:
    def image_tag(self):
        if self.photo:
            return mark_safe('<img src="/uploads/%s" width="300" height="150" style="object-fit: cover;"/>' % (self.photo))
        return 'Нет фото'
    image_tag.short_description = 'Фото'


class BrandModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    manufacturer_code = models.CharField('Код производителя', max_length=15, unique=True)
    country = models.CharField('Страна производителя', max_length=64, )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Technology(models.Model):
    title = models.CharField("Название", max_length=64)
    description = models.TextField("Описание", max_length=300)
    photo = models.ImageField("Фото", upload_to="technologies/")

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Технолгия'
        verbose_name_plural = 'Технологии'

# Обувь https://www.sportmaster.ru/product/22645790299/

class ShoesModel(models.Model):
    title = models.CharField('Название', max_length=128,)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    insulation_weight = models.PositiveIntegerField('Вес утеплителя, г/м2', null=True, blank=True) # число 
    clasp = models.CharField('Застежка', max_length=64)# ТЕКСТ 
    reinforced_bumper = models.BooleanField('Усиленный бампер')  # да или нет
    
    antibacterial_impregnation = models.CharField('Антибактериальная пропитка', max_length=64, blank=True)
    moisture_protection = models.CharField('Защита от влаги', max_length=64, blank=True)
    
    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    age_type = models.CharField('Возрастная категория', max_length=1, choices=AGE_TYPE)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE, blank=True)
    season = models.CharField('Сезон', max_length=1, choices=SEASON, blank=True)
    guarantee_period = models.PositiveIntegerField('Срок гарантии', null=True, blank=True)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара')

    upper_material = models.CharField('Материал верха', max_length=64, blank=True)
    lining_material = models.CharField('Материал подкладки', max_length=64, blank=True)
    outsole_material = models.CharField('Материал подошвы', max_length=64,blank=True)
    insole_material = models.CharField('Материал стельки', max_length=64, blank=True) # текст
    
    brand = models.ForeignKey(BrandModel, verbose_name="Бренд", on_delete=models.CASCADE, related_name='brand_shoes')
    technologies = models.ManyToManyField(Technology, verbose_name="Технологии", blank=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'


class ShoesPhotoModel(PhotoMixin, models.Model):
    photo = models.ImageField('Фото', upload_to='shoes/')
    shoes = models.ForeignKey(ShoesModel, on_delete=models.CASCADE, verbose_name="К обуви", related_name='photos')
    
    def __str__(self) -> str:
        return self.photo.path
    
    class Meta:
        verbose_name = 'Фото обуви'
        verbose_name_plural = 'Фото обуви'

#  КУРТКА https://www.sportmaster.ru/product/25367870299/

class JacketModel(models.Model):
    title = models.CharField('Название', max_length=128)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)

    model_parameters = models.CharField('Параметры модели', max_length=128, blank=True)
    product_size_on_model = models.CharField('Размер товара на модели ', max_length=128, blank=True )

    cut = models.CharField('Зауженный',max_length=64, blank=True) 
    possibility_of_packaging = models.CharField('Возможность упаковки', max_length=64, blank=True)
    length = models.CharField('Длина', max_length=64, blank=True)    
    
    ergonomic_cut = models.CharField('Эргономичный крой', max_length=64, blank=True)
    hood = models.CharField('Капюшон', max_length=64)
    сlasp = models.CharField('Застежка', max_length=64)
    taped_seams = models.CharField('Проклеенные швы', max_length=64, blank=True)
    number_of_pockets = models.CharField('Количество карманов', max_length=64)
    thumb_hole_in_cuff = models.CharField('Отверстие для большого пальца в манжете', max_length=64, blank=True)
    cuff_adjustment = models.CharField('Регулировка манжеты', max_length=64, blank=True)
    fur = models.CharField('Мех', max_length=64, blank=True)
# Функциональные особенности
    presence_of_membrane = models.CharField('Наличие мембраны', max_length=64, blank=True)
    water_repellent_impregnation = models.CharField('Водоотталкивающая пропитка', max_length=64, blank=True)
    waterproof_zippers = models.CharField('Водонепроницаемые молнии', max_length=64, blank=True)
    wind_protection = models.CharField('Защита от ветра', max_length=64)
    insulation = models.CharField('Утеплитель', max_length=64)
#Общие характеристики
    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    age_type = models.CharField('Возрастная категория', max_length=1, choices=AGE_TYPE)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    season = models.CharField('Сезон', max_length=1, choices=SEASON)
    guarantee_period = models.PositiveIntegerField('Срок гарантии', null=True, blank=True)      
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара') 
    
#СОСТАВ 
    upper_material = models.CharField('Материал верха', max_length=64)
    lining_material = models.CharField('Материал утеплителя', max_length=64)
    insole_material = models.CharField('Материал подкладки', max_length=64, blank=True)
# Дополнительные характеристики
    reflective_details = models.CharField('Светоотражающие детали', max_length=64, blank=True)
    brand = models.ForeignKey(BrandModel, verbose_name="Бренд", on_delete=models.CASCADE, related_name='brand_jacket')
    technologies = models.ManyToManyField(Technology, verbose_name="Технологии", blank=True)
    
#Уход за товаром
    care_instructions = models.CharField('Рекомендации по уходу', max_length=128, blank=True)
    additional_information = models.CharField('Дополнительная информация', max_length=350, blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Куртка'
        verbose_name_plural = 'Куртки'


class JacketPhotoModel(PhotoMixin, models.Model):
    photo = models.ImageField('Фото', upload_to='jackets/')
    jacket = models.ForeignKey(JacketModel, on_delete=models.CASCADE, verbose_name="К куртке", related_name='photos')

    def __str__(self) -> str:
        return self.photo.path
    
    class Meta:
        verbose_name = 'Фото куртке'
        verbose_name_plural = 'Фото куртке'

# Брюки  https://www.sportmaster.ru/product/29259240299/

class TrouserModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    model_parameters = models.CharField('Параметры модели (муж)', max_length=64)
    product_size_on_model = models.CharField('Размер товара на модели (муж)', max_length=64)

    сut = models.CharField('Покрой', max_length=64)
    waist = models.CharField('Талия', max_length=64)
    style = models.CharField('Фасон', max_length=64)
    clasp = models.CharField('Застежка', max_length=64)
    number_of_pockets = models.PositiveIntegerField('Количество карманов')
    
    presence_of_membrane = models.BooleanField('Наличие мембраны')
    water_repellent_impregnation = models.BooleanField('Наличие мембраны')

    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    age_type = models.CharField('Возрастная категория', max_length=1, choices=AGE_TYPE)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара')

    upper_material = models.CharField('Материал верха', max_length=64)

    care_instructions = models.CharField('Рекомендации по уходу', max_length=64)
    additional_information = models.CharField('Дополнительная информация', max_length=64)

    brand = models.ForeignKey(BrandModel, verbose_name="Бренд", on_delete=models.CASCADE, related_name='brand_trousersers')
    technologies = models.ManyToManyField(Technology, verbose_name="Технологии", blank=True)
    season = models.CharField('Сезон', max_length=1, choices=SEASON) 

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Брюки'
        verbose_name_plural = 'Брюки'


class TrouserPhotoModel(PhotoMixin, models.Model):
    photo = models.ImageField('Фото', upload_to='trousers/')
    trousers = models.ForeignKey(TrouserModel, on_delete=models.CASCADE, verbose_name="К Брюкам", related_name='photos')

    def __str__(self) -> str:
        return self.photo.path
    
    class Meta:
        verbose_name = 'Фото брюки'
        verbose_name_plural = 'Фото брюки'

# Термобелье  https://www.sportmaster.ru/product/29312690299/

class ThermalUnderwearModel(models.Model):
    title = models.CharField('Название', max_length=128,)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    model_parameters = models.CharField('Параметры модели', max_length=64, blank=True)
    product_size_on_model = models.CharField('Размер товара на модели', max_length=64, blank=True)

    сut = models.CharField('Покрой', max_length=64, blank=True)
    length = models.CharField('Длина', max_length=64, blank=True)
    flat_seams = models.BooleanField('Плоские швы')

    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    age_type = models.CharField('Возрастная категория', max_length=1, choices=AGE_TYPE)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара')

    materials = models.CharField('Материалы', max_length=64)

    brand = models.ForeignKey(BrandModel, verbose_name="Бренд", on_delete=models.CASCADE, related_name='brand_thermal')
    technologies = models.ManyToManyField(Technology, verbose_name="Технологии", blank=True)

    care_instructions = models.CharField('Рекомендации по уходу', max_length=64)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Термобелье'
        verbose_name_plural = 'Термобелье'
    

class ThermalUnderwearPhotoModel(PhotoMixin, models.Model):
    photo = models.ImageField('Фото', upload_to='thermal_underwear/')
    thermal_underwear = models.ForeignKey(ThermalUnderwearModel, on_delete=models.CASCADE, verbose_name="К Термобелье", related_name='photos')
    
    def __str__(self) -> str:
        return self.photo.path
    
    class Meta:
        verbose_name = 'Фото термобелье'
        verbose_name_plural = 'Фото термобелье'

#  https://www.sportmaster.ru/product/29299490299/  

class JumperModel(models.Model):
    title = models.CharField('Название', max_length=128)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    model_parameters = models.CharField('Параметры модели', max_length=64, blank=True)
    product_size_on_model = models.CharField('Размер товара на модели ', max_length=64, blank=True)

    сut = models.CharField('Покрой', max_length=64, blank=True)
    length = models.CharField('Длина', max_length=64, blank=True)
    the_length_of_the_sleeve = models.CharField('Длина рукава', max_length=64, blank=True)
    clasp = models.CharField('Застежка', max_length=64, blank=True)
    number_of_pockets = models.PositiveIntegerField('Количество карманов', null=True,  blank=True )

    material = models.CharField('Материал', max_length=64)

    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    age_type = models.CharField('Возрастная категория', max_length=1, choices=AGE_TYPE)
    season = models.CharField('Сезон', max_length=1, choices=SEASON)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара')

    upper_material = models.CharField('Материал верха', max_length=64, blank=True)
    lining_material = models.CharField('Материал утеплителя', max_length=64, blank=True)
    insole_material = models.CharField('Материал подкладки', max_length=64, blank=True)

    brand = models.ForeignKey(BrandModel, verbose_name="Бренд", on_delete=models.CASCADE, related_name='brand_jumper')
    technologies = models.ManyToManyField(Technology, verbose_name="Технологии", blank=True)
    care_instructions = models.CharField('Рекомендации по уходу', max_length=300, blank=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Джемпер'
        verbose_name_plural = 'Джемперы'


class JumperPhotoModel(PhotoMixin, models.Model):
    photo = models.ImageField('Фото', upload_to='jumper/')
    jumper = models.ForeignKey(JumperModel, on_delete=models.CASCADE, verbose_name="К Джемперу", related_name='photos')

    def __str__(self) -> str:
        return self.photo.path
    
    class Meta:
        verbose_name = 'Фото джемпер'
        verbose_name_plural = 'Фото джемпер'

CATEGORY = {
    'shoes': ShoesModel,
    'jacket': JacketModel,
    'trousers': TrouserModel,
    'thermal': ThermalUnderwearModel,
    'jumper': JumperModel,
}

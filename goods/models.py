from django.db import models




#БАЗА ДАННЫХ 


GENDER = [
    ('M', 'Мужской'),
    ('F', 'Женский')
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

class BrandModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    manufacturer_code = models.CharField('Код производителя', max_length=7, unique=True)
    country = models.CharField('Страна производителя', max_length=64, unique=True)

# Обувь

class ShoesModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    insulation_weight = models.PositiveIntegerField('Вес утеплителя, г/м2')
    clasp = models.CharField('Застежка', max_length=64)
    reinforced_bumper = models.BooleanField('Усиленный бампер')    
    
    antibacterial_impregnation = models.CharField('Антибактериальная пропитка', max_length=64)
    moisture_protection = models.CharField('Защита от влаги', max_length=64)
    
    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    season = models.CharField('Сезон', max_length=1, choices=SEASON)
    
    guarantee_period = models.PositiveIntegerField('Срок гарантии')
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара', max_length=64)
    category =  models.CharField('Категория', max_length=64)

    upper_material = models.CharField('Материал верха', max_length=64)
    lining_material = models.CharField('Материал подкладки', max_length=64)
    outsole_material = models.CharField('Материал подошвы', max_length=64)
    insole_material = models.CharField('Материал стельки', max_length=64)
    
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, verbose_name="Бренд", related_name='brand')


class ShoesPhotoModel(models.Model):
    photo = models.ImageField('Фото', upload_to='shoes/')
    shoes = models.ForeignKey(ShoesModel, on_delete=models.CASCADE, verbose_name="К обуви", related_name='photos')

#  КУРТКА 

class JacketModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)

    cut = models.CharField('Зауженный',max_length=64) 
    possibility_of_packaging = models.CharField('Возможность упаковки', max_length=64)
    length = models.BooleanField('Длина',mmax_length=64)    
    
    ergonomic_cut = models.CharField('Эргономичный крой', max_length=64)
    hood = models.CharField('Капюшон', max_length=64)
    Clasp = models.CharField('Застежка', max_length=64)
    taped_seams = models.CharField('Проклеенные швы', max_length=64)
    number_of_pockets = models.CharField('Количество карманов', max_length=64)
    thumb_hole_in_cuff = models.CharField('Отверстие для большого пальца в манжете', max_length=64)
    cuff_adjustment = models.CharField('Регулировка манжеты', max_length=64)
    fur = models.CharField('Мех', max_length=64)
    
    presence_of_membrane = models.CharField('Наличие мембраны', max_length=64)
    water_repellent_impregnation = models.CharField('Водоотталкивающая пропитка', max_length=64)
    waterproof_zippers = models.CharField('Водонепроницаемые молнии', max_length=64)
    wind_protection = models.CharField('Защита от ветра', max_length=64)
    insulation = models.CharField('Утеплитель', max_length=64)
    
    kind_of_sport = models.CharField('Вид спорта', max_length=64)
    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    season = models.CharField('Сезон', max_length=1, choices=SEASON) 
    
#Общие характеристики
    guarantee_period = models.PositiveIntegerField('Срок гарантии', max_length=64)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара', max_length=64)
    category =  models.CharField('Категория', max_length=64)
    
#СОСТАВ 
    upper_material = models.CharField('Материал верха', max_length=64)
    lining_material = models.CharField('Материал утеплителя', max_length=64)
    insole_material = models.CharField('Материал стельки', max_length=64)
    reflective_details = models.CharField('Светоотражающие детали', max_length=64)
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, verbose_name="Бренд", related_name='brand')
    
#Уход за товаром
    care_instructions = models.CharField('Рекомендации по уходу', max_length=64)
    additional_information = models.CharField('Дополнительная информация', max_length=64)



class JacketPhotoModel(models.Model):
    photo = models.ImageField('Фото', upload_to='jackets/')
    jacket = models.ForeignKey(JacketModel, on_delete=models.CASCADE, verbose_name="К куртке", related_name='photos')

#остальные штаны

class TrousersModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)

    insulation = models.CharField('Утеплитель',max_length=64) 
    
    
    
    possibility_of_packaging = models.CharField('Возможность упаковки', max_length=64)
    length = models.BooleanField('Длина',mmax_length=64)    
    
    ergonomic_cut = models.CharField('Эргономичный крой', max_length=64)
    hood = models.CharField('Капюшон', max_length=64)
    Clasp = models.CharField('Застежка', max_length=64)
    taped_seams = models.CharField('Проклеенные швы', max_length=64)
    number_of_pockets = models.CharField('Количество карманов', max_length=64)
    Thumb_hole_in_cuff = models.CharField('Отверстие для большого пальца в манжете', max_length=64)
    cuff_adjustment = models.CharField('Регулировка манжеты', max_length=64)
    Fur = models.CharField('Мех', max_length=64)
    
    Presence_of_membrane = models.CharField('Наличие мембраны', max_length=64)
    water_repellent_impregnation = models.CharField('Водоотталкивающая пропитка', max_length=64)
    waterproof_zippers = models.CharField('Водонепроницаемые молнии', max_length=64)
    wind_protection = models.CharField('Защита от ветра', max_length=64)
    insulation = models.CharField('Утеплитель', max_length=64)
    
    Kind_of_sport = models.CharField('Вид спорта', max_length=64)
    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    season = models.CharField('Сезон', max_length=1, choices=SEASON) 
    
#Общие характеристики
    guarantee_period = models.PositiveIntegerField('Срок гарантии', max_length=64)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара', max_length=64)
    category =  models.CharField('Категория', max_length=64)
    
#СОСТАВ 
    upper_material = models.CharField('Материал верха', max_length=64)
    lining_material = models.CharField('Материал утеплителя', max_length=64)
    insole_material = models.CharField('Материал стельки', max_length=64)
    reflective_details = models.CharField('Светоотражающие детали', max_length=64)
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, verbose_name="Бренд", related_name='brand')
    
#Уход за товаром
    Care_instructions = models.CharField('Рекомендации по уходу', max_length=64)
    additional_information = models.CharField('Дополнительная информация', max_length=64)


class jacketPhotoModel(models.Model):
    photo = models.ImageField('Фото', upload_to='shoes/')
    trousers = models.ForeignKey(TrousersModel, on_delete=models.CASCADE, verbose_name="К Брюка", related_name='photos')



# class Technology(models.Model):
#     pass
    # many-to-many 
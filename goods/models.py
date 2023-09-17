from django.db import models


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


# Остальные



# class Technology(models.Model):
#     pass
    # many-to-many 
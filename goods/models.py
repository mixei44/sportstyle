


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

# Обувь https://www.sportmaster.ru/product/22645790299/

class ShoesModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    insulation_weight = models.PositiveIntegerField('Вес утеплителя, г/м2') # число 
    clasp = models.CharField('Застежка', max_length=64) # ТЕКСТ 
    reinforced_bumper = models.BooleanField('Усиленный бампер')  # да или нет
    
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


# Брюки  https://www.sportmaster.ru/product/29259240299/

class TrousersModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    model_parameters = models.CharField('Параметры модели (муж)', max_length=64)
    product_size_on_model = models.CharField('Размер товара на модели (муж)', max_length=64)

    сut = models.CharField('Покрой', max_length=64)
    waist = models.CharField('Талия', max_length=64)
    style = models.CharField('Фасон', max_length=64)
    clasp = models.CharField('Застежка', max_length=64)
    Number_of_pockets = models.PositiveIntegerField('Количество карманов')
    
    presence_of_membrane = models.BooleanField('Наличие мембраны')
    water_repellent_impregnation = models.BooleanField('Наличие мембраны')

    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    kind_of_sport = models.CharField('Вид спорта', max_length=64)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара', max_length=64)
    category =  models.CharField('Категория', max_length=64)

    upper_material = models.CharField('Материал верха', max_length=64)

    care_instructions = models.CharField('Рекомендации по уходу', max_length=64)
    additional_information = models.CharField('Дополнительная информация', max_length=64)

    season = models.CharField('Сезон', max_length=1, choices=SEASON) 

class TrousersPhotoModel(models.Model):
    photo = models.ImageField('Фото', upload_to='trousers/')
    trousers = models.ForeignKey(TrousersModel, on_delete=models.CASCADE, verbose_name="К Брюкам", related_name='photos')


# Термобелье  https://www.sportmaster.ru/product/29312690299/

class ThermalUnderwearModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    model_parameters = models.CharField('Параметры модели (муж)', max_length=64)
    product_size_on_model = models.CharField('Размер товара на модели (муж)', max_length=64)

    сut = models.CharField('Покрой', max_length=64)
    length = models.CharField('Длина', max_length=64)
    flat_seams = models.BooleanField('Плоские швы')

    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    kind_of_sport = models.CharField('Вид спорта', max_length=64)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара', max_length=64)
    category =  models.CharField('Категория', max_length=64)

    materials = models.CharField('Застежка', max_length=64)

    care_instructions = models.CharField('Рекомендации по уходу', max_length=64)

class ThermalUnderwearPhotoModel(models.Model):
    photo = models.ImageField('Фото', upload_to='thermal_underwear/')
    thermal_underwear = models.ForeignKey(ThermalUnderwearModel, on_delete=models.CASCADE, verbose_name="К Термобелье", related_name='photos')


#  https://www.sportmaster.ru/product/29299490299/  

class JumperModel(models.Model):
    title = models.CharField('Название', max_length=128, unique=True)
    price = models.PositiveIntegerField('Цена')
    description = models.TextField('Описание', max_length=2048)
    
    model_parameters = models.CharField('Параметры модели (муж)', max_length=64)
    product_size_on_model = models.CharField('Размер товара на модели (муж)', max_length=64)

    сut = models.CharField('Покрой', max_length=64)
    length = models.CharField('Длина', max_length=64)
    the_length_of_the_sleeve = models.CharField('Длина рукава', max_length=64)
    clasp = models.CharField('Застежка', max_length=64)
    Number_of_pockets = models.PositiveIntegerField('Количество карманов')

    material = models.CharField('Материал', max_length=64)

    gender = models.CharField('Пол', max_length=1, choices=GENDER)
    kind_of_sport = models.CharField('Вид спорта', max_length=64)
    sport_type = models.CharField('Вид спорта', max_length=1, choices=SPORT_TYPE)
    product_authenticity_guarantee = models.BooleanField('Гарантия подлинности товара', max_length=64)
    category =  models.CharField('Категория', max_length=64)

    upper_material = models.CharField('Материал верха', max_length=64)

    care_instructions = models.CharField('Рекомендации по уходу', max_length=64)

class JumperPhotoModel(models.Model):
    photo = models.ImageField('Фото', upload_to='jumper/')
    jumper = models.ForeignKey(JumperModel, on_delete=models.CASCADE, verbose_name="К Джемперу", related_name='photos')
















































# class Technology(models.Model):
#     pass
    # many-to-many 
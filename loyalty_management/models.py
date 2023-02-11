from django.db import models


class Card(models.Model):
	STATUS = (
		(0, 'Не активирована'),
		(1, 'Активирована'),
		(2, 'Просрочена'),
		(3, 'В корзине'),
	)

	serial_number = models.CharField(max_length=3, verbose_name='Серия (3 цифры)')
	number = models.CharField(max_length=8, verbose_name='Номер (8 цифр)')
	date1 = models.DateTimeField(verbose_name='Дата выпуска')
	date2 = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')
	last_use = models.DateTimeField(blank=True, null=True, verbose_name='Дата последнего использования')
	total_sum = models.FloatField(default=0, verbose_name='Сумма покупок')
	status = models.IntegerField(choices=STATUS, default=0, verbose_name='Статус')
	discount = models.FloatField(default=1, verbose_name='Текущая скидка')

	class Meta:
		verbose_name = 'Карта'
		verbose_name_plural = 'Карты'

	def __str__(self):
		return f'{self.serial_number} {self.number}'


class Order(models.Model):
	card = models.ForeignKey(Card, related_name='orders', on_delete=models.CASCADE, verbose_name='Карта')
	number = models.CharField(max_length=6, verbose_name='Номер')
	date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
	order_sum = models.FloatField(default=0, verbose_name='Сумма')
	discount = models.FloatField(default=0, verbose_name='Процент скидки')
	discount_sum = models.FloatField(default=0, verbose_name='Сумма скидки')

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

	def __str__(self):
		return self.number


class Product(models.Model):
	order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE, verbose_name='Заказ')
	name = models.CharField(max_length=30, verbose_name='Наименование')
	price = models.FloatField(verbose_name='Цена')
	discount_price = models.FloatField(default=0, verbose_name='Цена со скидкой')

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'

	def __str__(self):
		return self.name

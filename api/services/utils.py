from datetime import datetime, timezone
from random import randint

from loyalty_management.models import Card, Order, Product
from api.serializers import CardFullInfoSerializer, OrderInfoSerializer, ProductInfoSerializer


CARD_FIELDS = ['serial_number', 'number', 'date1', 'date2', 'last_use', 'total_sum', 'status', 'discount']
ORDER_FIELDS = ['number', 'date', 'order_sum', 'discount', 'discount_sum']


def check_cards_status(cards):
	"""Обновляет статус карты на 'Просрочено' при истечении срока действия"""

	now = datetime.now(timezone.utc)
	for card in cards:
		if card.date2:
			# если текущая дата превышает date2 и статус 'Не активирована' или 'Активирована'
			# меняем статус на 'Просрочена'
			if now > card.date2 and card.status in [0, 1]:
				card.status = 2
				card.save()


def generate_card_number(serial_number):
	"""Генерирует уникальный для опрделенной серии номер карты"""

	all_cards = Card.objects.filter(serial_number=serial_number)
	all_numbers = [card.number for card in all_cards]
	while True:
		number = ''
		for _ in range(8):
			number += str(randint(0, 9))
		if number not in all_numbers:
			break

	return number


def generate_order_number():
	"""Генерирует уникальный номер заказа"""

	all_orders = Order.objects.all()
	all_numbers = [order.number for order in all_orders]
	while True:
		number = ''
		for _ in range(6):
			number += str(randint(0, 9))
		if number not in all_numbers:
			break
	
	return number


def str_to_datetime(date_string):
	"""Преобразует строку в дату и время"""

	return datetime(
		year=int(date_string[:4]),
		month=int(date_string[5:7]),
		day=int(date_string[8:10]),
		hour=int(date_string[11:13]),
		minute=int(date_string[14:16]),
		second=0,
		microsecond=0
	)


def check_serial_number(serial_number):
	"""Проверка корректности параметра serial_number"""

	if serial_number is None:
		return 'Нет параметра serial_number'
	elif len(serial_number) != 3:
		return 'Недопустимое значение параметра serial_number'
	return ''


def check_number(number):
	"""Проверка корректности параметра number"""

	if number is None:
		return 'Нет параметра number'
	elif len(number) != 8:
		return 'Недопустимое значение параметра number'
	return ''


def check_both_params(serial_number, number):
	"""Проверяет корректность параметров serial_number и number"""

	message1 = check_serial_number(serial_number)
	message2 = check_number(number)

	if message1 != '' and message2 != '':
		return f'{message1}; {message2}'
	elif message1 != '':
		return message1
	elif message2 != '':
		return message2
	else:
		if not Card.objects.filter(serial_number=serial_number, number=number).exists():
			return f'Карты с параметрами serial_number={serial_number}, number={number} не существует'
		else:
			return ''


def search_cards(search_params):
	"""Поиск карт по параметрам с сортировкой"""

	kwargs = {}
	# находим совпадения между возможными полями карты и именами переданных в запросе параметров
	common_params = list(set(CARD_FIELDS) & set(search_params.keys()))

	for param in common_params:
		value = search_params[param]
		if param == 'date1':
			kwargs.update({'date1__gte': str_to_datetime(value)})
		elif param == 'date2':
			kwargs.update({'date2__lte': str_to_datetime(value)})
		else:
			kwargs.update({param: value})

	order = search_params.get('order', 'date1')
	cards = Card.objects.filter(**kwargs)
	check_cards_status(cards)
	
	# проверяем корректность параметра сортировки
	# параметр должен совпадать с одним из CARD_FIEDS и теми же полями со знаком -
	if order in CARD_FIELDS + ['-' + i for i in CARD_FIELDS]:
		cards = cards.order_by(order)

	return cards


def get_card_full_info(serial_number, number, order_by):
	"""Полная информация о карте, заказaх и продуктах в виде словаря"""

	card = Card.objects.get(serial_number=serial_number, number=number)
	check_cards_status([card])

	response = {'response': 'ok'}
	response.update(CardFullInfoSerializer(card).data)
	response.update({'orders': []})

	# получаем заказы с сортировкой
	orders = Order.objects.filter(card=card)
	if order_by in ORDER_FIELDS + ['-' + i for i in ORDER_FIELDS]:
		orders = orders.order_by(order_by)

	# добавляем информацию о заказах
	for order in orders:
		order_info = OrderInfoSerializer(order).data
		products = Product.objects.filter(order=order)
		order_info.update({'products': []})
		for product in products:
			product_info = ProductInfoSerializer(product).data
			order_info['products'].append(product_info)
		response['orders'].append(order_info)

	return response


def update_card_status(serial_number, number, status):
	"""Обновление статуса карты"""

	if status is None:
		return {'response': 'error', 'message': 'Нет параметра status'}
	elif not int(status) in [0, 1, 2, 3]:
		return {'response': 'error', 'message': 'Недопустимое значение параметра status'}
	status = int(status)

	card = Card.objects.get(serial_number=serial_number, number=number)
	card.status = status
	card.save()
	response = {'response': 'ok'}
	response.update(CardFullInfoSerializer(card).data)
	return response


def create_card(data):
	"""Создание карты"""

	card = Card()
	card.serial_number = data['serial_number']
	card.number = generate_card_number(card.serial_number)
	date1 = data.get('date1', None)
	if date1 == '' or date1 is None:
		card.date1 = datetime.now()
	else:
		card.date1 = str_to_datetime(date1)
	date2 = data.get('date2', None)
	if date2 is None or date2 == '':
		card.date2 = None
	else:
		card.date2 = str_to_datetime(date2)
	card.status = data.get('status', 0)
	card.discount = data.get('discount', 2.5)
	card.save()

	response = {'response': 'ok'}
	response.update(CardFullInfoSerializer(card).data)

	return response


def delete_card(serial_number, number, to_trash):
	"""Удаление карты в корзину или полностью"""

	card = Card.objects.get(serial_number=serial_number, number=number)
	if to_trash:
		card.status = 3
		card.save()
	else:
		card.delete()

	return {'response': 'ok'}


def add_order(data):
	"""Добавление информации о заказе на карту. Расчет скидки"""

	card = Card.objects.get(serial_number=data['serial_number'], number=data['number'])

	# если карта не активирована, прочрочена или находится в корзине
	if card.status != 1:
		return {'response': 'error', 'message': 'Карта должна быть активирована'}

	# получаем данные о продуктах
	# структура: {'products': [{'name': '', 'price': '', 'discount_price': ''}, ...]}
	products = data.get('products', None)
	if products is None:
		return {'response': 'error', 'message': 'Нет параметра products'}
	
	# создаем новый заказ
	order = Order()
	order.card = card
	order.number = generate_order_number()
	order.date = datetime.now()
	order.order_sum = 0
	order.discount = card.discount
	order.discount_sum = 0

	# проходим по всем продуктам
	for pr in products:
		product = Product()
		product.order = order
		product.name = pr['name']
		product.price = pr['price']
		product.discount_price = pr['discount_price']
		order.save()
		product.save()

		# если на продукт есть скидка, добавляем скидочную цену в общую
		if product.discount_price != 0:
			order.order_sum += product.discount_price
		else:
			# добавляем цену к общей сумме
			# рассчитываем скидку для даннго продукта
			order.order_sum += product.price
			order.discount_sum += round(product.price * order.discount / 100, 2)
	
	 # отнимаем получившуюся скидку от общей стоимости
	order.order_sum -= order.discount_sum
	order.order_sum = round(order.order_sum, 2)
	order.save()

	# обновляем данные в карте
	card.total_sum += order.order_sum
	card.total_sum = round(card.total_sum, 2)
	card.last_use = datetime.now()

	# обновляем процент скидки на основе общей суммы покупок
	if card.total_sum <= 100:
		card.discount = 2.5
	elif card.total_sum <= 150:
		card.discount = 3.0
	elif card.total_sum <=200:
		card.discount = 3.5
	elif card.total_sum <= 250:
		card.discount = 4.0
	elif card.total_sum <= 350:
		card.discount = 4.5
	else:
		card.discount = 5.0
	card.save()

	response = {'response': 'ok'}
	response.update(OrderInfoSerializer(order).data)

	return response

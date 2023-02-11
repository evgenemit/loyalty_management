from rest_framework import generics
from rest_framework.response import Response

from .services import utils
from .serializers import CardInfoSerializer
from .paginations import CardsPagination

from loyalty_management.models import Card


class CardsListAPIView(generics.ListAPIView):
	"""Список всех карт с сортировкой"""
	serializer_class = CardInfoSerializer
	pagination_class = CardsPagination

	def get_queryset(self):
		order = self.request.GET.get('order', 'date1')
		cards = Card.objects.all()
		utils.check_cards_status(cards)
		cards = cards.order_by(order)

		return cards


class CardAPIView(generics.GenericAPIView):
	"""Полная информация о карте, заказах и продуктах"""

	def get(self, request):
		serial_number = request.GET.get('serial_number', None)
		number = request.GET.get('number', None)
		order = request.GET.get('order', 'date')

		check_params_message = utils.check_both_params(serial_number, number)
		if check_params_message == '':
			return Response(utils.get_card_full_info(serial_number, number, order))
		else:
			return Response({'response': 'error', 'message': check_params_message})


class CardsSearchAPIView(generics.ListAPIView):
	"""Поиск карт по параметрам с сортировкой"""
	serializer_class = CardInfoSerializer
	pagination_class = CardsPagination

	def get_queryset(self):
		return utils.search_cards(self.request.GET)


class UpdateStatusAPIView(generics.GenericAPIView):
	"""Обновление статуса карты"""

	def post(self, request):
		serial_number = request.data.get('serial_number', None)
		number = request.data.get('number', None)
		status = request.data.get('status', None)
		
		check_params_message = utils.check_both_params(serial_number, number)
		if check_params_message == '':
			return Response(utils.update_card_status(serial_number, number, status))
		else:
			return Response({'response': 'error', 'message': check_params_message})


class CreateCardAPIView(generics.GenericAPIView):
	"""Создание карты"""

	def post(self, request):
		serial_number = request.data.get('serial_number', None)

		check_params_message = utils.check_serial_number(serial_number)
		if check_params_message == '':
			return Response(utils.create_card(request.data))
		else:
			return Response({'response': 'error', 'message': check_params_message})


class DeleteCardAPIView(generics.GenericAPIView):
	"""Удаление карты в корзину или полное"""

	def post(self, request):
		to_trash = True if request.data.get('to_trash', False) == 'true' else False
		serial_number = request.data.get('serial_number', None)
		number = request.data.get('number', None)

		check_params_message = utils.check_both_params(serial_number, number)
		if check_params_message == '':
			return Response(utils.delete_card(serial_number, number, to_trash))
		else:
			return Response({'response': 'error', 'message': check_params_message})


class AddOrderAPIView(generics.GenericAPIView):
	"""Добавление информации о заказе на карту"""

	def post(self, request):
		serial_number = request.data.get('serial_number', None)
		number = request.data.get('number', None)

		check_params_message = utils.check_both_params(serial_number, number)
		if check_params_message == '':
			return Response(utils.add_order(request.data))
		else:
			return Response({'response': 'error', 'message': check_params_message})

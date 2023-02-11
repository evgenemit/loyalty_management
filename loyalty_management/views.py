from django.shortcuts import render


def cards(request):
	return render(request, 'loyalty_management/cards.html')


def card_profile(request, serial_number, number):
	return render(request, 'loyalty_management/card.html', {'serial_number': serial_number, 'number': number})


def generator(request):
	return render(request, 'loyalty_management/generator.html')


def trash(request):
	return render(request, 'loyalty_management/trash.html')

let serial_number = window.location.href.slice(-13, -10)
let number = window.location.href.slice(-9, -1)
let order = '-date'
let page = 0
let max_page = 0
let orders = []
let to_trash = true
let to_status = '0'


function update_order() {
    $('#page-number').text(page)

    const order = orders[page - 1]
    $('#order-number').text(order['number'])
    $('#order-date').text(order['date'].replace('T', ' ').replace('Z', '').slice(0, 19))
    $('#order-sum').html(order['order_sum'] + ' <span>BYN</span>')
    $('#order-discount').text(order['discount'] + ' %')
    $('#order-discount-sum').html(order['discount_sum'] + ' <span>BYN</span>')

    $('.products').html('')
    order['products'].forEach(product => {
        $('.products').append(`
            <div class="row border-bottom">
                <p class="col-4">${product['name']}</p>
                <p class="col-2">${product['price']} <span>BYN</span></p>
                ${(product['discount_price'] !== 0) ? `<p class="col">${product['discount_price']} <span>BYN</span></p>` : ''}
            </div>`)
    });
}


function display_order() {
    if (max_page === 0) {
        $('#history').append('<p class="text-secondary">Заказов нет</p>')
    }
    else {
        $('#max-page').text(max_page)
        update_order()
        $('#orders').fadeIn(200)
    }
}


function update_cards() {
    $.ajax({
        url: `/api/card/`,
        method: 'GET',
        data: {
            'serial_number': serial_number,
            'number': number,
            'order': order,
        },
        success: function(response) {
            if (response['response'] === 'error') {
                $('#error-message').fadeIn(200)
            }
            else {
                orders = response['orders']
                update_order()
            }
        }
    })
}


$.ajax({
    url: `/api/card/`,
    method: 'GET',
    data: {
        'serial_number': serial_number,
        'number': number,
        'order': order
    },
    success: function(response) {
        if (response['response'] === 'error') {
            $('#error-message').fadeIn(200)
        }
        else {
            max_page = response['orders'].length
            if (max_page > 0) {
                page = 1
                $('#max-page').text(max_page)
            }
            orders = response['orders']

            $('#serial_number').text(response['serial_number'])
            $('#number').text(response['number'])
            $('#date1').text(response['date1'].replace('T', ' ').replace('Z', '').slice(0, 19))
            if (response['date2'] === null) {
                $('#date2').text('Не ограничено')
            }
            else {
                $('#date2').text(response['date2'].replace('T', ' ').replace('Z', '').slice(0, 19))
            }
            if (response['last_use'] === null) {
                $('#last_use').text('Не использовалась')
            }
            else {
                $('#last_use').text(response['last_use'].replace('T', ' ').replace('Z', '').slice(0, 19))
            }
            $('#total_sum').html(response['total_sum'] + ' <span>BYN</span>')
            switch (response['status']) {
                case 0:
                    $('#status').text('Не активирована')
                    break;
                case 1:
                    $('#status').text('Активирована')
                    break;
                case 2:
                    $('#status').text('Просрочена')
                    break;
                case 3:
                    $('#status').text('В корзине')
                    break;
            }
            $('#discount').text(response['discount'] + ' %')

            if (response['status'] === 3) {
                $('#modal-delete-card').text('Удалить карту')
                to_trash = false
            }
            else
                $('#modal-delete-card').text('В корзину')
            $('.content').fadeIn(200)
            display_order()
        }
    }
})

$('#next').click(function(e) {
    e.preventDefault()
    if (page < max_page) {
        page += 1
        update_order()
    }
})


$('#prev').click(function(e) {
    e.preventDefault()
    if (page > 1) {
        page -= 1
        update_order()
    }
})

$('.sort span').click(function(e) {
    e.preventDefault()

    if (order === 'date' || order === '-date') {
        $('#sort-date').removeClass('text-primary').addClass('text-secondary')
    } else if (order === 'order_sum' || order === '-order_sum') {
        $('#sort-sum').removeClass('text-primary').addClass('text-secondary')
    } else if (order === 'discount' || order === '-discount') {
        $('#sort-discount').removeClass('text-primary').addClass('text-secondary')
    } else if (order === 'discount_sum' || order === '-discount_sum') {
        $('#sort-discount-sum').removeClass('text-primary').addClass('text-secondary')
    }

    switch ($(this).attr('id')) {
        case 'sort-date':
            if (order === 'date')
                order = '-date'
            else
                order = 'date'
            $('#sort-date').removeClass('text-secondary').addClass('text-primary')
            break;
        case 'sort-sum':
            if (order === 'order_sum')
                order = '-order_sum'
            else
                order = 'order_sum'
            $('#sort-sum').removeClass('text-secondary').addClass('text-primary')
            break;
        case 'sort-discount':
            if (order === 'discount')
                order = '-discount'
            else
                order = 'discount'
            $('#sort-discount').removeClass('text-secondary').addClass('text-primary')
            break;
        case 'sort-discount-sum':
            if (order === 'discount_sum')
                order = '-discount_sum'
            else
                order = 'discount_sum'
            $('#sort-discount-sum').removeClass('text-secondary').addClass('text-primary')
            break;
    }
    update_cards()
})

$('#delete-card').click(function(e) {
    $.ajax({
        url: `/api/card/delete/`,
        method: 'POST',
        data: {
            'serial_number': serial_number,
            'number': number,
            'to_trash': (to_trash ? 'true' : 'false'),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(response) {
            if (response['response'] === 'ok') {
                if (to_trash) {
                    window.location.reload()
                }
                else {
                    window.location.replace(`/`)
                }
            }
        }
    })
})

$('#update-card').click(function(e) {
    to_status = $('select').val()
    $.ajax({
        url: `/api/card/update-status/`,
        method: 'POST',
        data: {
            'serial_number': serial_number,
            'number': number,
            'status': to_status,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            if (response['response'] === 'ok') {
                window.location.reload()
            }
        }
    })
})

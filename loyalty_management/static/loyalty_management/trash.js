$('#header-trash').addClass('btn-green').removeClass('btn-white-green')

let page = 1
let max_page = 0
let order = '-date1'


function update_cards_table(cards) {
    $('.cards').html('')
    $('#page-number').text(page)
    cards.forEach(card => {
        $('.cards').append(`
        <div class="row pb-1 pt-1 border-bottom">
            <div class="col-1">${card['serial_number']}</div>
            <div class="col"><a href="/card/${card['serial_number']}/${card['number']}/">${card['number']}</a></div>
            <div class="col">${card['date1'].replace('T', ' ').replace('Z', '').slice(0, 19)}</div>
            <div class="col">${(card['date2'] === null) ? 'Не ограничено' : card['date2'].replace('T', ' ').replace('Z', '').slice(0, 19)}</div>
        </div>`)
    })
    if (cards.length > 0) {
        $('#trash').fadeIn(200)
    }
    else {
        $('#error-message').fadeIn(200)
    }
    $('.cards > div:last').removeClass('border-bottom')
}

function update_cards() {
    $.ajax({
        url: '/api/cards/search/',
        method: 'GET',
        data: {
            'status': 3,
            'page': page,
            'order': order
        },
        success: function(response) {
            max_page = Math.ceil(response['count'] / 10)
            $('#max-page').text(max_page)
            update_cards_table(response['results'])
        }
    })
}


update_cards()


$('#next').click(function(e) {
    e.preventDefault()
    if (page < max_page) {
        $.ajax({
            url: '/api/cards/search/',
            method: 'GET',
            data: {
                'status': 3,
                'page': page + 1,
                'order': order
            },
            success: function(response) {
                page += 1
                update_cards_table(response['results'])
            }
        })
    }
})


$('#prev').click(function(e) {
    e.preventDefault()
    if (page > 1) {
        $.ajax({
            url: '/api/cards/search/',
            method: 'GET',
            data: {
                'status': 3,
                'page': page - 1,
                'order': order
            },
            success: function(response) {
                page -= 1
                update_cards_table(response['results'])
            }
        })
    }
})


$('.cards-table > div:first > div').click(function(e) {
    e.preventDefault()

    if (order === 'serial_number' || order === '-serial_number') {
        $('#serial-number-btn').removeClass('text-primary').addClass('text-secondary')
    } else if (order === 'number' || order === '-number') {
        $('#number-btn').removeClass('text-primary').addClass('text-secondary')
    } else if (order === 'date1' || order === '-date1') {
        $('#date1-btn').removeClass('text-primary').addClass('text-secondary')
    } else if (order === 'date2' || order === '-date2') {
        $('#date2-btn').removeClass('text-primary').addClass('text-secondary')
    }

    switch ($(this).attr('id')) {
        case 'serial-number-btn':
            if (order === 'serial_number')
                order = '-serial_number'
            else
                order = 'serial_number'
            $('#serial-number-btn').removeClass('text-secondary').addClass('text-primary')
            break;
        case 'number-btn':
            if (order === 'number')
                order = '-number'
            else
                order = 'number'
            $('#number-btn').removeClass('text-secondary').addClass('text-primary')
            break;
        case 'date1-btn':
            if (order === 'date1')
                order = '-date1'
            else
                order = 'date1'
            $('#date1-btn').removeClass('text-secondary').addClass('text-primary')
            break;
        case 'date2-btn':
            if (order === 'date2')
                order = '-date2'
            else
                order = 'date2'
            $('#date2-btn').removeClass('text-secondary').addClass('text-primary')
            break;
    }

    update_cards()
})

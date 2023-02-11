$('#header-generator').addClass('btn-green').removeClass('btn-white-green')

let serial_number
let date1
let date2

$('#count input').val('')
$('#serial-number input').val('')
$('#date1').val('')
$('#date2').val('')

$('form').submit(function(e) {
    e.preventDefault()
    const count = parseInt($('#count input').val())
    serial_number = $('#serial-number input').val()
    date1 = $('#date1').val()
    date2 = $('#date2').val()
    for (let i = 0; i < count; i++) {
        $.ajax({
            url: '/api/card/create/',
            method: 'POST',
            data: {
                'serial_number': serial_number,
                'date1': date1,
                'date2': date2,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response['response'] === 'ok') {
                    $('#count input').val('')
                    $('#serial-number input').val('')
                    $('#date1').val('')
                    $('#date2').val('')
                    $('button').addClass('disabled').focusout()
                }
            }
        })
    }
})

$('#count input, #serial-number input').keyup(function() {
    if ($('#count input').val() !== '' && $('#serial-number input').val() !== '')
        $('button').removeClass('disabled')
    else
        $('button').addClass('disabled')
})

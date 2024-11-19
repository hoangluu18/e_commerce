function add_to_cart(event, id, name, price) {
    event.preventDefault();
    fetch('/api/add_to_cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (res) {
        console.info(res)
        return res.json()
    }).then(function (data) {
        console.info(data)

        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++) {
            counter[i].innerText = data.total_quantity
        }
        counter.innerText = data.total_quantity
    }).catch(function (err){
        console.error(err)
    })
}

function pay(){
    if (confirm('Ban chac chan muon thanh toan khong?') == true){
        fetch('/api/pay', {
            method: 'post',

        }).then(res => res.json()).then( data => {
            if (data.code == 200)
                location.reload()
        }).catch(err => console.error(err))
    }
}

function updateCart(id, obj) {
    fetch('/api/update_cart', {
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(
        data => {
            let counter = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < counter.length; i++) {
                counter[i].innerText = data.total_quantity
            }

            let amount = document.getElementById('total-amount')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)
        }
        ).catch(err => console.error(err))

}

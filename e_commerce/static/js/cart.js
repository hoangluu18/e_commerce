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

        let counter = document.getElementsByClassName('cart-badge')
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
function deleteCart(id) {
    if(confirm("Ban chac chan muon xoa san pham nay khong?") == true){
        fetch('/api/delete-cart/' + id, {
            method: 'delete',
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
                let e = document.getElementById("product" + id)
                e.style.display = 'none'
            }
            ).catch(err => console.error(err))
    }

}

function addComment(productId){
    let content = document.getElementById('commentId')
    if (content !== null){
        fetch('/api/comments',{
            method: 'post',
            body: JSON.stringify({
                'product_id': productId,
                'content': content.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data =>{
            if (data.status == 201){
                let c = data.comment
                let area = document.getElementById('commentArea')
                area.innerHTML = `
                    <div class="row">
                        <div class="col-md-1 col-xs-4">
                            <img src="${c.user.avatar}" alt="demo" class="img-fluid rounded-circle">
                        </div>
                        <div class="col-md-11 col-xs-8">
                            <p>${c.content}</p>
                            <p><em>${moment(c.created_date).locale('vi').fromNow()}</em></p>
                        </div>
                   </div>
                ` + area.innerHTML
            }else  if (data.status == 404){
                alert(data.err_msg)
            }
        })
    }
}

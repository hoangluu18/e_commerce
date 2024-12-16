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

function addToCartAndRedirect(event, id, name, price) {
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
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let counter = document.getElementsByClassName('cart-badge');
        for (let i = 0; i < counter.length; i++) {
            counter[i].innerText = data.total_quantity;
        }
        // After cart is updated, redirect
        window.location.href = '/cart';
    }).catch(function(err) {
        console.error(err);
    });
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

function addComment(productId) {
    let content = document.getElementById('commentId')
    if (content !== null && content.value.trim() !== '') {
        // Show loading


        fetch('/api/comments', {
            method: 'post',
            body: JSON.stringify({
                'product_id': productId,
                'content': content.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (data.status == 201) {
                let c = data.comment;
                let area = document.getElementById('commentArea');

                // Create new comment element
                const newComment = `
                    <div class="comment-item" style="opacity: 0; transform: translateY(20px);" xmlns="http://www.w3.org/1999/html">
                        <div class="comment-user">
                            <div class="comment-avatar">
                                <img src="${c.user.avatar || '/static/images/default.jpg'}" 
                                     alt="${c.user.name || 'User'}">
                            </div>
                            <div class="user-info">
                            <strong
                                <span class="text-dark username">${c.user.name}</span>
                             </strong>
                                <em class="comment-date">${moment(c.created_date).locale('vi').fromNow()}</em>
                            </div>
                        </div>
                        <div class="comment-content">
                            <p>${c.content}</p>
                        </div>
                    </div>
                `;

                area.innerHTML = newComment + area.innerHTML;

                // Animate new comment
                const newCommentEl = area.firstElementChild;
                requestAnimationFrame(() => {
                    newCommentEl.style.transition = 'all 0.3s ease';
                    newCommentEl.style.opacity = '1';
                    newCommentEl.style.transform = 'translateY(0)';
                });

                // Clear input
                content.value = '';


            } else {

            }
        }).catch(error => {
            console.error('Error:', error);

        });
    } else {
        Console.log('Empty comment');
    }
}

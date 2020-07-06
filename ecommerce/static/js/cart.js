var updateBtns = document.getElementsByClassName('update-cart')

// looping through the button length and on each iteration get the queryset
for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:' , productId, 'action:', action)


        // if the user is logged in, items are sent to the database
        // if the user is not logged, data is sent t0 the browser and stored there
        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else {
            updateUserOrder(productId, action)

        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data')

        // url to send the POST data to
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        // sending the objects as a string
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    // return a promise to get a response
    .then(response => {
        return response.json();
    })
    // .then((response) => {
    //     if (response.status >= 200 && response.status <= 299) {
    //         return response.json();
    //     } else {
    //         throw Error(response.statusText);
    //     }
    // })
    // .then((jsonResponse) => {
    //     // do whatever you want with the JSON response
    .then((data) => {
        // console.log('data:', data)
        location.reload()
    // }).catch((error) => {
    //     // Handle the error
    //     console.log(error);
    // });
    });
}

function addCookieItem(productId, action){
    console.log('User is not logged in')
    // add or remove items 
    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productId];
        }
        
    }

    console.log('Cart', cart)
    // updating the cookie when the page reloads and retaining the information
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

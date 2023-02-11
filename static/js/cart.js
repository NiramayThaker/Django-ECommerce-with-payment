let updateBtns = document.getElementsByClassName('update-cart')

for (const element of updateBtns) {
    element.addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productID:', productId, 'action:', action)
        // user = this.dataset.user
        console.log(user)

        if (user === 'AnonymousUser') {
            console.log("User not logged in")
        } else {
            console.log("User not logged in")
        }
    })
}


// let updateBtns = document.getElementsByClassName('update-cart')
//
// for (let i = 0; i < updateBtns.length; i++) {
//     updateBtns[i].addEventListener('click', function () {
//         let productId = this.dataset.product
//         let action = this.dataset.action
//         console.log('productID:', productId, 'action:', action)
//     })
// }

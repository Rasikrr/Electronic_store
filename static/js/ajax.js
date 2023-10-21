document.addEventListener("DOMContentLoaded", function() {
    const cartLenObj = document.getElementById("cart-len");
    addToCart(cartLenObj)
    function addToCart(cartLenObj) {
        fetch(`/check_cart`)
                .then(response => response.json())
                .then(data => {
                    const cartLen = data.cart_len;
                    console.log(cartLen)
                    if(cartLen == "0"){
                        cartLenObj.style.display = "none";
                    }

                });
        }
});



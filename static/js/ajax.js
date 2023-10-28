document.addEventListener("DOMContentLoaded", function() {
    const cartLenObj = document.getElementById("cart-len");
    addToCart(cartLenObj)
    function addToCart(cartLenObj) {
        fetch(`/check_cart`)
                .then(response => response.json())
                .then(data => {
                    const cartLen = data.cart_len;
                    if(cartLen == "0"){
                        cartLenObj.style.display = "none";
                    } else {
						cartLenObj.textContent = cartLen;
					}

                });
        }
});

document.addEventListener("DOMContentLoaded", function() {
	const cartLenObj = document.querySelector(".qty");
	const cartLen = cartLenObj.querySelectorAll(".product-widget").length
	console.log("cart len ",cartLen);

});


document.addEventListener("DOMContentLoaded", function(){
    const addToCartButton = document.getElementById("add-cart-btn");
    const messageContainer = document.getElementById("message-container");

	addToCartButton.addEventListener("click", function() {
		let IsInStock = document.querySelector(".product-available");
		if (IsInStock.textContent != "In Stock") {
			alert("Item is out of stock")
		} else {
			const productId = this.getAttribute("data-product-id");
			addToCart(productId, IsInStock);
		}

	});


    function addToCart(productId, IsInStock_obj) {
        fetch(`/add_to_cart/${productId}`)
            .then(response => response.json())
            .then(data => {
				const quantity = data.quantity
				let cartList = document.querySelector(".cart-list"); // Получаем элемент cart-list
				if(quantity == "1"){
					console.log("YES")
					const prodId = productId;
					const prodName = data.name;
					const prodImage = data.image;
					const prodQuantity = quantity;
					const prodPrice = data.price;
					const prodCategory = data.category;
					cartList = document.querySelector(".cart-list"); // Получаем элемент cart-list
					const cartItem = createCartItem(prodId, prodImage, prodQuantity, prodPrice, prodCategory, prodName);
					cartList.appendChild(cartItem)
				} else {
					const cartItem = document.querySelector(`[data-product-id="${productId}"]`).closest(".cart-list")
					const qty_obj = cartItem.querySelector(`[prod-id="${productId}"]`)
					changeQty(qty_obj);
				}
				const product_qty_in_stock = data.quantity_in_stock
				if(product_qty_in_stock == "0"){
					IsInStock_obj.textContent = "Out Of Stock";
					IsInStock_obj.style.color = "red";
				}
				changeCartLength(cartList);
                showMessage(data.message);
				ChangePriceOverall(data.price);
            });
    }
	function changeCartLength(cartList){
		const productWidgets = cartList.querySelectorAll(".product-widget"); // Получаем дочерние элементы с классом "product-widget"
		const cartLen = document.getElementById("cart-len")
		const itemSelected = document.querySelector(".item-selected")
		cartLen.style.display = "block"
		const len = productWidgets.length
		itemSelected.textContent = len + " " + itemSelected.textContent.substring(1, itemSelected.textContent.length)
		cartLen.textContent = len;
	}
    function showMessage(message) {
        const messageElement = document.createElement("p");
        if (message == 'You have to sign in before adding item to cart'){
            alert(message)
        } else {
            messageElement.textContent = message;
            messageContainer.appendChild(messageElement);
            messageElement.style.color = "green";
            messageElement.style.fontWeight = "bold";
        }
    }
	function changeQty(qty_obj){
		let num = parseInt(qty_obj.textContent.substring(0, qty_obj.textContent.length - 1))+1;
		qty_obj.textContent = num+'x';
	}

	function createCartItem(prodId, prodImage, prodQuantity, prodPrice, prodCategory, prodName){
		// Создаем элемент <div> с классом "product-widget"
		const productWidget = document.createElement("div");
		productWidget.className = "product-widget";
		// Вставляем содержимое шаблона product_widget_template.html, заменяя переменные значениями из контекста
		productWidget.innerHTML =`
        <div class="product-img">
            <img src="${prodImage}" alt="">
        </div>
        <div class="product-body">
            <h3 class="product-name">
                <a href="/${prodCategory.toLowerCase()}/product/${prodId}">
                    ${prodName}
                </a>
            </h3>
            <h4 class="product-price">
                <span class="qty" prod-id="${prodId}">${prodQuantity}x</span>
                $${prodPrice}
            </h4>
        </div>
        <button class="delete" data-product-id="${prodId}">
            <i class="fa fa-close"></i>
        </button>
		`;
		return productWidget;
	}

	function ChangePriceOverall(price){
		const CartOverall = document.getElementById("cart-overall")
		let CurrentOverall = Number(CartOverall.textContent.substring(11,CartOverall.textContent.length))
		CartOverall.textContent = `SUBTOTAL: $${CurrentOverall + Number(price)}`;
	}
});


// Cart Overall
document.addEventListener("DOMContentLoaded", function (){
	let OverallPrice = 0;
	const CartOverall = document.getElementById("cart-overall")
	const cartList = document.querySelector(".cart-list");
	const productWidgets = cartList.querySelectorAll(".product-widget"); // Получаем дочерние элементы с классом "product-widget"
	for(i = 0; i<productWidgets.length;i+=1){
		const quantity_obj = productWidgets[i].querySelector(".qty")
		const quantity = Number(quantity_obj.textContent.substring(0, quantity_obj.textContent.length-1));
		const price_obj = productWidgets[i].querySelector(".price")
		const price = Number(price_obj.textContent.substring(1, price_obj.textContent.length));
		OverallPrice += price*quantity;
	}
	CartOverall.textContent = `SUBTOTAL: $${OverallPrice}`;

});


document.addEventListener("DOMContentLoaded",
	function () {
		const DeleteFromCart = document.querySelectorAll(".delete")
		DeleteFromCart.forEach(button => {
			button.addEventListener("click", function () {
				const productId = button.getAttribute("data-product-id");
				const cartList = document.querySelector(".cart-list");
				function delete_from_cart(productId) {
					fetch(`/delete_from_cart/${productId}`)
						.then(response => response.json())
						.then(data => {
							quantity = Number(data.quantity)
							price = Number(data.price)
							cartList.removeChild(button.parentNode)
							ChangeOverallPrice(price * quantity)
						});
				}

				delete_from_cart(productId);
				changeCartLength();
				console.log(productId);
				console.log(button.parentNode)
			});
		});

		function ChangeOverallPrice(price) {
			const CartOverall = document.getElementById("cart-overall")
			let CurrentOverall = Number(CartOverall.textContent.substring(11, CartOverall.textContent.length))
			CurrentOverall -= price;
			CartOverall.textContent = `SUBTOTAL: $${CurrentOverall}`;
		}

		function changeCartLength() {
			const cartLen = document.getElementById("cart-len")
			const itemSelected = document.querySelector(".item-selected")
			const NewCartLen = Number(cartLen.textContent) - 1
			cartLen.textContent = NewCartLen;
			itemSelected.textContent = `${NewCartLen} Item(s) selected`
			if(NewCartLen == "0"){
				cartLen.style.display = "none";
			}
		}
	});


document.addEventListener("DOMContentLoaded", function (){
	const wishlistObj = document.getElementById("wish-list-len");
	function check_wishlist(){
		fetch(`/check_wishlist`)
			.then(response => response.json())
			.then(data => {
				const wishlist_len = data.wishlist_len;
				if(wishlist_len == "0"){
					wishlistObj.style.display = "none";
				}
			});
		}
	check_wishlist();
});
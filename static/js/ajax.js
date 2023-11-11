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


document.addEventListener("DOMContentLoaded", function () {
    const cartList = document.querySelector(".cart-list");

    cartList.addEventListener("click", function (event) {
        const button = event.target.closest(".delete");
        if (button) {
            const productId = button.getAttribute("data-product-id");

            function delete_from_cart(productId) {
                fetch(`/delete_from_cart/${productId}`)
                    .then(response => response.json())
                    .then(data => {
                        const quantity = Number(data.quantity);
                        const price = Number(data.price);
                        button.parentNode.remove(); // Удаляем родительский узел кнопки
                        ChangeOverallPrice(price * quantity);
                        changeCartLength();
                    });
            }

            delete_from_cart(productId);
            console.log(productId);
        }
    });

    function ChangeOverallPrice(price) {
        const CartOverall = document.getElementById("cart-overall");
        let CurrentOverall = Number(CartOverall.textContent.substring(11));
        CurrentOverall -= price;
        CartOverall.textContent = `SUBTOTAL: $${CurrentOverall}`;
    }

    function changeCartLength() {
        const cartLen = document.getElementById("cart-len");
        const itemSelected = document.querySelector(".item-selected");
        const NewCartLen = Number(cartLen.textContent) - 1;
        cartLen.textContent = NewCartLen;
        itemSelected.textContent = `${NewCartLen} Item(s) selected`;
        if (NewCartLen === 0) {
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
				} else{
					wishlistObj.textContent = wishlist_len;
				}
			});
		}
	check_wishlist();
});

document.addEventListener("DOMContentLoaded", function(){
	let priceMin = document.getElementById("price-min");
	let priceMax = document.getElementById("price-max");
	let priceSlider = document.getElementById("price-slider");

	function getQueryParams() {
        const urlParams = new URLSearchParams(window.location.search);
        return {
            priceMin: urlParams.get('price-min'),
            priceMax: urlParams.get('price-max')
        };
    }
	const queryParams = getQueryParams()
	if (queryParams.priceMin && queryParams.priceMax) {
        priceMin.value = queryParams.priceMin;
        priceMax.value = queryParams.priceMax;
		const minVal = parseInt(queryParams.priceMin);
        const maxVal = parseInt(queryParams.priceMax);
		priceSlider.noUiSlider.set([minVal, maxVal])
	}

});

document.addEventListener("DOMContentLoaded", function(){
	const addToWishlistButtons = document.querySelectorAll(".add-to-wishlist");
	addToWishlistButtons.forEach(button => {
		button.addEventListener('click', function(){
			const productId = button.getAttribute("id-product");
			let heartIcon = button.querySelector('i');
			let heartIconClassList = heartIcon.classList
			if(heartIconClassList[1] == "fa-heart-o"){
				heartIconClassList.remove("fa-heart-o");
				heartIconClassList.add("fa-heart")
			} else {
				heartIconClassList.remove("fa-heart");
				heartIconClassList.add("fa-heart-o")
			}
			heartIcon.classList = heartIconClassList;
			fetch(`/add_to_wishlist/${productId}`)
				.then(response => response.json())
				.then(data => {
					const is_created = data.is_created;
					if(is_created == "false"){
						console.log("false");
					}else {
						const message = data.message;
						const prodName = data.name;
						const prodPrice = data.price;
						const prodId = data.id;
						const prodImage = data.image;
						const prodCategory = data.category;
						let wishList = document.querySelector(".wishlist-list"); // Получаем элемент cart-list
						const wishListItem = createWishListItem(prodId, prodImage, prodPrice, prodName, prodCategory);
						wishList.appendChild(wishListItem);
						const wishListQty = document.getElementById("wish-list-len")
						const wishListItemSelected = document.querySelector(".wishlist-item-selected");
						changeQty(wishListQty, wishListItemSelected, "add");
					}
				});
		});
	});
	function createWishListItem(prodId, prodImage, prodPrice, prodName, prodCategory){
		// Создаем элемент <div> с классом "product-widget"
		const productWidget = document.createElement("div");
		productWidget.className = "product-widget";
		// Вставляем содержимое шаблона product_widget_template.html, заменяя переменные значениями из контекста
		productWidget.innerHTML =`
        <div class="product-widget" id-product="${prodId}">
			<div class="product-img">
				<img src="${prodImage}" alt="">
			</div>
			<div class="product-body">
				<h3 class="product-name">
					<a href="/${prodCategory.toLowerCase()}/product/${prodId}">
						"${prodName}"
					</a>
				</h3>
			</div>
			<button class="delete" id-product="${prodId}"><i class="fa fa-close"></i></button>
		</div>
		`;
		return productWidget;
	}

	function changeQty(wishListQty, wishListItemSelected, add_or_delete){
		let cur_len = parseInt(wishListQty.textContent);
		console.log(cur_len)
		if(isNaN(cur_len)){
			console.log("YYYYY")
			wishListQty.style.display = "inline";
		}
		if(add_or_delete == "add"){
			if(isNaN(cur_len)){
				cur_len = 0;
			}
			cur_len += 1;
		} else{
			cur_len -= 1;
		}
		wishListItemSelected.textContent = `${cur_len} Item(s)`;

		wishListQty.textContent = cur_len;
	}
});


document.addEventListener("DOMContentLoaded", function () {
	const wishList = document.querySelector(".wishlist-list");

	wishList.addEventListener("click", function (event) {
		const button = event.target.closest(".delete");
		if (button) {
			const productId = button.getAttribute("id-product");
			console.log(productId)

			function delete_from_wishlist(productId) {
				fetch(`/delete_from_wishlist/${productId}`)
					.then(response => response.json())
					.then(data => {
						const message = data.message;
						const wishlist_len = data.wishlist_len;
						changeWishlistLen(wishlist_len);
						console.log(message);
						console.log(wishlist_len);
						button.parentNode.remove(); // Удаляем родительский узел кнопки
					});
			}

			delete_from_wishlist(productId);
			console.log(productId);
		}
	});
	function changeWishlistLen(wishlist_len){
		const wishlistQty = document.getElementById("wish-list-len");
		const wishlistItemSelected = document.querySelector(".wishlist-item-selected");
		wishlistItemSelected.textContent = `${wishlist_len} Item(s)`;
		if(wishlist_len == "0"){
			wishlistQty.style.display = "none";
		} else {
			wishlistQty.textContent = wishlist_len;
		}
	}

});

document.addEventListener("DOMContentLoaded", function () {
  const totalObj = document.querySelector(".order-total");
  const total = totalObj.textContent.substring(1, totalObj.textContent.length);
  const placeOrderBtn = document.getElementById("make-order");

  placeOrderBtn.addEventListener("click", function(e) {
    if(total == "0") {
      e.preventDefault();
      alert("You have to add some items in Your cart before making order");
    }
  });
});

document.addEventListener("DOMContentLoaded", function(){


});
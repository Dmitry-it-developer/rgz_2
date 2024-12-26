document.addEventListener("DOMContentLoaded", function () {
        
    const apiUrl = "/json-rpc-api/";
    const cart = [];
    const cartContent = document.getElementById("cart-content");
    const cartTotalPrice = document.getElementById("cart-total-price");
    const payButton = document.getElementById("pay-button")
    if (payButton) {
        payButton.onclick = () => payCart();
    }
    
    async function fetchFurnitureData() {
        const payload = {
            jsonrpc: "2.0",
            method: "list",
            id: 1
        };

        const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
        });

        const data = await response.json();

        populateTable(data.result);
    }

    function populateTable(furniture) {
        const tableBody = document.getElementById("furniture-table-body");
        tableBody.innerHTML = "";
        const hasActionColumn = document.querySelector("thead th:nth-child(4)") !== null;
        furniture.forEach(item => {
            const row = document.createElement("tr");

            const nameCell = document.createElement("td");
            nameCell.textContent = item.name;

            const descriptionCell = document.createElement("td");
            descriptionCell.textContent = item.description;

            const priceCell = document.createElement("td");
            priceCell.textContent = `${item.price} руб.`;

            row.appendChild(nameCell);
            row.appendChild(descriptionCell);
            row.appendChild(priceCell);

            if (hasActionColumn) {
                const actionCell = document.createElement("td");
                const addToCartButton = document.createElement("button");
                addToCartButton.textContent = "Добавить";
                addToCartButton.className = "cart-button";
                addToCartButton.onclick = () => addToCart(item);
                actionCell.style.padding = '0px 0px'; 
                actionCell.appendChild(addToCartButton);
                row.appendChild(actionCell);
            }

            tableBody.appendChild(row);
        });
    };
    fetchFurnitureData();

    function addToCart(item) {
        cart.push(item);
        updateCart();
    };

    function updateCart() {
        const cartContent = document.getElementById("cart-content");
        cartContent.innerHTML = "";
    
        if (cart.length === 0) {
            const emptyRow = document.createElement("tr");
            const emptyCell = document.createElement("td");
            emptyCell.colSpan = 3;
            emptyCell.textContent = "Ваша корзина пуста.";
            emptyRow.appendChild(emptyCell);
            cartContent.appendChild(emptyRow);
        } else {
            cart.forEach((item, index) => {
                const row = document.createElement("tr");
    
                const nameCell = document.createElement("td");
                nameCell.textContent = item.name;
    
                const priceCell = document.createElement("td");
                priceCell.textContent = `${item.price} руб.`;
    
                const actionCell = document.createElement("td");
                const removeButton = document.createElement("button");
                removeButton.textContent = "Удалить";
                removeButton.className = "cart-remove-button";
                removeButton.onclick = () => removeFromCart(index);
    
                actionCell.appendChild(removeButton);
                row.appendChild(nameCell);
                row.appendChild(priceCell);
                row.appendChild(actionCell);
    
                cartContent.appendChild(row);
            });
        }
    
        const total = cart.reduce((sum, item) => sum + item.price, 0);
        document.getElementById("cart-total-price").textContent = `${total} руб.`;
        document.getElementById("pay-button").disabled = cart.length === 0;
    };
    function removeFromCart(index) {
        cart.splice(index, 1);
        updateCart();
    };
    async function payCart() {
        cart.length = 0;
        updateCart();
        alert('Оплата прошла успешно!')
    };

});
function showLogin() {
    const authBlock = document.getElementById("auth-content");
    authBlock.innerHTML = `
        <h2>Вход</h2>
        <form id="login-form" onsubmit="submitLogin(event)">
            <label for="login-username">Логин:</label>
            <input type="text" id="login-username" name="username" ><br>
            <label for="login-password">Пароль:</label>
            <input type="password" id="login-password" name="password" ><br>
            <div id="login-error" class="auth-error"></div>
            <button type="submit" class="auth-button">Войти</button>
            <button type="button" class="auth-button secondary" onclick="resetAuthBlock()">Отмена</button>
        </form>
    `;
}

function showRegister() {
    const authBlock = document.getElementById("auth-content");
    authBlock.innerHTML = `
        <h2>Регистрация</h2>
        <form id="register-form" onsubmit="submitRegister(event)">
            <label for="register-username">Логин:</label>
            <input type="text" id="register-username" name="username" ><br>
            <label for="register-password">Пароль:</label>
            <input type="password" id="register-password" name="password" ><br>
            <div id="register-error" class="auth-error"></div>
            <button type="submit" id="register-button" class="auth-button">Зарегистрироваться</button>
            <button type="button" class="auth-button secondary" onclick="resetAuthBlock()">Отмена</button>
        </form>
    `;
}

function resetAuthBlock() {
    const authBlock = document.getElementById("auth-content");
    authBlock.innerHTML = `
        <button class="auth-button" onclick="showLogin()">Вход</button>
        <button class="auth-button" onclick="showRegister()">Регистрация</button>
    `;
}

async function submitLogin(event) {
    event.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (data.error) {
        document.getElementById("login-error").innerText = data.error.message || "Ошибка входа.";
    } else {
        location.reload(); 
    }
}

async function submitRegister(event) {
    event.preventDefault();
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (data.error) {
        document.getElementById("register-error").innerText = data.error.message || "Ошибка регистрации.";
    } else {
        location.reload(); 
    }
}
async function logout() {
    const response = await fetch("/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });

    const data = await response.json();
    if (data.message) {
        location.reload();
    }
}
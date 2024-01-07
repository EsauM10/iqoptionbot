class Cards {
    static getHTML(){
        return `
        <section class="cards">
            <div class="card card-profit">
                <header>
                    <i class="ph ph-currency-circle-dollar"></i>
                    <h1>Lucro</h1>
                </header>
                <main>
                    <h1 id="assetProfit">$ 0.00</h1>
                </main>
            </div>
    
            <div class="card">
                <header>
                    <i class="ph ph-chart-pie-slice"></i>
                    <h1>Operações</h1>
                </header>
            </div>
    
            <div class="card card-alerts">
                <header>
                    <div>
                        <i class="ph ph-bell-ringing"></i>
                        <h1>Alertas</h1>
                    </div>
                    <aside>
                        <input id="priceAlertInput" type="number" value="0.00000" step="0.00002" required="true" min="0">
                        <button id="addAlertButton">
                            <i class="ph ph-plus"></i>
                        </button>
                    </aside>
                </header>
                <ul id="alertList"></ul>
            </div>
        </section>
        `
    }
}

class Logs {
    static getHTML() {
        return `
            <section class="logs">
                <header>
                    <i class="ph ph-article"></i>
                    <h1>Logs</h1>
                </header>
                <ul id="logList"></ul>
            </section>
        `
    }
}

class Transactions {
    static getHTML() {
        return `
            <aside class="history">
                <header>
                    <i class="ph ph-clock-counter-clockwise"></i>
                    <h1>Histórico de Trading</h1>
                </header>
                <ul id="transactionList"></ul>
            </aside>
        `
    }
}


/**
 * @param {{id: number, price: number}} alert
 * @param {() => void} onClick 
 * @returns 
 */
function alertItem(alert, onClick) {
    const li = document.createElement("li")
    const icon = document.createElement("i")
    
    li.id = `alert${alert.id}`
    icon.classList.add("ph", "ph-x", "pointer")
    icon.addEventListener("click", onClick)
    
    li.innerHTML = `
        <div>
            <i class="ph ph-bell"></i>
            <p>${alert.price.toFixed(5)}</p>
        </div>
    `
    li.appendChild(icon)
    return li
}

/**
 * @param {string} assetName 
 * @returns 
 */
function assetOption(assetName) {
    const option = document.createElement("option")
    option.value = assetName
    option.innerText = assetName
    return option
}

/**
 * @param {{id: number, date: string, message: string}} log 
 * @returns 
 */
function logItem(log) {
    const li = document.createElement("li")
    li.innerHTML = `
        <div class="logDate">${log.date}</div>
        <div class="logMessage">${log.message}</div>
    `
    return li
}

/**
 * @param {{
 *  id: number,
 *  asset: string,
 *  hour: string,
 *  value: number,
 *  profit: number,
 *  direction: string,
 *  is_completed: boolean
 * }} transaction 
 * @returns 
 */
function transactionItem(transaction) {
    const getProfitStyle = () => transaction.profit > 0 ? "positive" : "negative"
    const getDirectionStyle = () => {
        return transaction.direction === "CALL" ? "up positive" : "down negative"
    }

    const getStatusContent = () => {
        return transaction.is_completed 
        ? `<p class="${getProfitStyle()}">$ ${transaction.profit}</p>`
        : '<i class="ph ph-hourglass-high status"></i>'
    } 

    const li = document.createElement("li")
    li.classList.add("transactionItem")
    li.innerHTML = `
        <span>${transaction.hour}</span>
        <main>
            <div>
                <h1>${transaction.asset}</h1>
                <p>Binária</p>
            </div>
            <div>
                ${getStatusContent()}
                <p>$ ${transaction.value}</p>
            </div>
        </main>
        <i class="ph ph-arrow-${getDirectionStyle()}"></i>
    `
    return li
}

/**
 * @param {{name: string, icon: string, active: boolean}} item 
 * @param {() => void} onClick
 * @returns 
 */
function menuItem(item, onClick){
    const li = document.createElement("li")
    li.classList.add("menuItem")
    li.innerHTML = `<i class="${item.icon}"></i>`
    li.setAttribute("data-name", item.name)

    if(item.active) {
        li.classList.add("active")
    }
    
    li.addEventListener("click", onClick)
    return li
}
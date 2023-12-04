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

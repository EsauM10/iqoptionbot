const openAssetsSelect = document.getElementById("openAssets")
const accountBalance   = document.getElementById("accountBalance")

class HomePage {
    /**
     * @param {*} socket
     * @param {string} name 
     * @param {string} icon 
     * @param {boolean} active 
     */
    constructor(socket, name, icon, active) {
        this.socket = socket
        this.name   = name
        this.icon   = icon
        this.active = active
        this.startButton  = undefined
        this.assetRunning = false

        this.socket.on("addAlertItem", (data) => this.addAlertItem(data))
        this.socket.on("deleteAlertItem", (alertId) => this.deleteAlertItem(alertId))

        this.socket.on("setAccountBalance", (accountBalance) => this.setAccountBalance(accountBalance))
        this.socket.on("setTransactions", (transactions) => this.setTransactions(transactions))
        this.socket.on("setOpenAssets", (data) => this.setOpenAssets(data.selectedAsset, data.openAssets))
        
        this.socket.on("setAssetName", (data) => this.setAssetName(data.name))
        this.socket.on("setCurrencies", (data) => this.setCurrencies(data.name, data.currency1, data.currency2))
        this.socket.on("setAlerts", (data) => this.setAlerts(data.name, data.alerts))
        this.socket.on("setProfit", (data) => this.setProfit(data.name, data.profit))
        this.socket.on("setLogs", (data) => this.setLogs(data.name, data.logs))
        this.socket.on("setPrice", (data) => this.setPrice(data.name, data.price))
        this.socket.on("setPriceAlertInput", (data) => this.setPriceAlertInput(data.name, data.price))
        this.socket.on("updateStartButton", (data) => this.updateStartButton(data))

        openAssetsSelect.addEventListener("change", () => {
            const selectedAsset = this.getSelectedAsset()
            this.socket.emit("updateSelectedAsset", selectedAsset)
        })
    }

    /** @param {{id: number, price: number}} alert */
    addAlertItem(alert) {
        alertList.appendChild(alertItem(alert, () => {
            this.socket.emit("alerts", {
                method: "DELETE",
                payload: {alert_id: alert.id}
            })
        }))
    }

    /** @param {number} alertId */
    deleteAlertItem(alertId) {
        const alertItem = document.getElementById(`alert${alertId}`)
        if(alertItem) { 
            document.getElementById("alertList").removeChild(alertItem)
        }
    }

    createStartButton() {
        const buttonId = "startButton"
        const startButton = document.createElement("button")
        startButton.id = buttonId
        startButton.addEventListener("click", () => {
            if(this.assetRunning){
                this.socket.emit("stopBot")
                return
            }
            this.socket.emit("startBot", this.getSelectedAsset())
        })
        document.getElementById("assetHeader").appendChild(startButton)
        return startButton
    }

    /** @param {boolean} running */
    updateStartButtonContent(running) {
        this.startButton.innerHTML = running 
        ? "<i class='ph ph-stop'></i> Parar" 
        : "<i class='ph ph-play'></i> Iniciar";
    }

    /**
     * @param {{name: string, is_open: boolean, running: boolean}} data
     */
    updateStartButton(data) {
        this.assetRunning = data.running
        if(this.startButton === undefined){
            this.startButton = this.createStartButton()
        }
        if(this.getSelectedAsset() === data.name){
            if(!data.is_open) {
                this.removeStartButton()
                return
            }
            this.updateStartButtonContent(this.assetRunning)
        }
    }

    removeStartButton() {
        const assetHeader = document.getElementById("assetHeader")
        if(assetHeader){
            assetHeader.removeChild(this.startButton)
            this.startButton = undefined
        }
    }
    
    /** @returns {string} */
    getSelectedAsset() {
        return openAssetsSelect.value
    }

    /** @param {number} value */
    setAccountBalance(value) {
        accountBalance.innerText = `$ ${value}`
    }

    /** @param {string} name */
    setAssetName(name) {
        const assetName = document.getElementById("assetName")
        if(assetName && this.getSelectedAsset() === name){
            assetName.innerText = name
        }
    }

    /**
     * @param {string} name 
     * @param {string} currency1Url 
     * @param {string} currency2Url
     * @returns 
     */
    setCurrencies(name, currency1Url, currency2Url) {
        const currencies = document.getElementById("currencies")
        if(!currencies || this.getSelectedAsset() !== name){
            return
        }
        currencies.innerHTML = `
            <img src="${currency1Url}" alt="">
            <img src="${currency2Url}" alt="">
        `
    }

    /**
     * @param {string} assetName 
     * @param {{id: number, date: string, message: string}[]} logs 
     */
    setLogs(assetName, logs) {
        const logList = document.getElementById("logList")
        if(!logList || this.getSelectedAsset() !== assetName){
            return
        }
        
        logList.querySelectorAll("li").forEach(li => logList.removeChild(li))
        logs.forEach(log => {
            logList.appendChild(logItem(log))
        })
    }

    setTransactions(transactions) {
        const transactionList = document.getElementById("transactionList")
        if(!transactionList) {
            return
        }
        transactionList.querySelectorAll("li").forEach(li =>  transactionList.removeChild(li))
        transactions.forEach((transaction) => {
            transactionList.appendChild(transactionItem(transaction))
        })
    }

    /**
     * @param {string} assetName 
     * @param {{id: number, price: number}[]} alerts 
     */
    setAlerts(assetName, alerts) {
        const alertList = document.getElementById("alertList")
        if(!alertList || this.getSelectedAsset() !== assetName){
            return
        }
        alertList.querySelectorAll("li").forEach(li =>  alertList.removeChild(li))
        alerts.forEach(alert => this.addAlertItem(alert))
    }

    /**
     * @param {string} assetName 
     * @param {number} price 
     */
    setPrice(assetName, price) {
        const assetPrice = document.getElementById("assetPrice")
        if(assetPrice && this.getSelectedAsset() === assetName){
            assetPrice.innerText = price.toFixed(6)
        }
    }

    /**
     * @param {string} assetName 
     * @param {number} profit 
     */
    setProfit(assetName, profit) {
        const assetProfit = document.getElementById("assetProfit")
        if(assetProfit && this.getSelectedAsset() === assetName){
            assetProfit.innerText = `$ ${profit.toFixed(2)}`
        }
    }
    
    /**
     * @param {string} assetName 
     * @param {number} price 
     */
    setPriceAlertInput(assetName, price) {
        const priceAlertInput = document.getElementById("priceAlertInput")
        if(priceAlertInput && this.getSelectedAsset() === assetName){
            priceAlertInput.value = price.toFixed(5)
        }
    }

    /**
     * @param {string} selectedAsset 
     * @param {string[]} openAssets 
     */
    setOpenAssets(selectedAsset, openAssets) {
        openAssetsSelect.querySelectorAll("option").forEach(option =>  openAssetsSelect.removeChild(option))
        openAssets.forEach(asset => openAssetsSelect.appendChild(assetOption(asset)))
        openAssetsSelect.value = selectedAsset
    }

    render() {
        this.startButton = undefined
        document.getElementById("page").innerHTML = this.getHTML()
        document.getElementById("addAlertButton").addEventListener("click", () => {
            const alertPrice = document.getElementById("priceAlertInput").value
            const selectedAsset = this.getSelectedAsset()
            this.socket.emit("alerts", {
                method: "POST",
                payload: {
                    asset_name: selectedAsset, 
                    price: alertPrice}
            })
        })

        this.socket.emit("updateData") 
    }

    getHTML() {
        return `
        <main class="asset-content">
            <header id="assetHeader">
                <div class="assetInfo">
                    <div id="currencies">
                        <div class="loader"></div>
                    </div>
                    <div>
                        <h1 id="assetName"></h1>
                        <h2 id="assetPrice"></h2>
                    </div>
                </div>
            </header>
            ${Cards.getHTML()}
            ${Logs.getHTML()}
        </main>
        ${Transactions.getHTML()}
        `
    }
}

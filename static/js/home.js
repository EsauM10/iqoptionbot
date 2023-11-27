const openAssetsSelect = document.getElementById("openAssets")
const accountBalance   = document.getElementById("accountBalance")
const assetName        = document.getElementById("assetName")
const assetPrice       = document.getElementById("assetPrice")
const assetProfit      = document.getElementById("assetProfit")
const alertList        = document.getElementById("alertList")
const addAlertButton   = document.getElementById("addAlertButton")
const priceAlertInput  = document.getElementById("priceAlertInput")
const logList          = document.getElementById("logList")
const transactionList  = document.getElementById("transactionList")


class HomePage {
    constructor() {
        this.socket = io()
        this.startButton === undefined
        this.assetRunning = false

        this.socket.on("connect", () => {
            this.socket.emit("updateData")
        })
        
        this.socket.on("redirect", (pathname) => {
            console.log(pathname)
            redirect(pathname)})

        this.socket.on("addAlertItem", (data) => this.addAlertItem(data))
        this.socket.on("deleteAlertItem", (alertId) => this.deleteAlertItem(alertId))

        this.socket.on("setAccountBalance", (accountBalance) => this.setAccountBalance(accountBalance))
        this.socket.on("setTransactions", (transactions) => this.setTransactions(transactions))
        this.socket.on("setOpenAssets", (data) => this.setOpenAssets(data.selectedAsset, data.openAssets))
        
        this.socket.on("setAssetName", (data) => this.setAssetName(data.name))
        this.socket.on("setAlerts", (data) => this.setAlerts(data.name, data.alerts))
        this.socket.on("setProfit", (data) => this.setProfit(data.name, data.profit))
        this.socket.on("setLogs", (data) => this.setLogs(data.name, data.logs))
        this.socket.on("setPrice", (data) => this.setPrice(data.name, data.price))
        this.socket.on("setPriceAlertInput", (data) => this.setPriceAlertInput(data.name, data.price))
        this.socket.on("updateStartButton", (data) => {
            this.assetRunning = data.running
            if(this.startButton === undefined){
                this.startButton = this.createStartButton()
            }
            if(this.getSelectedAsset() === data.name){
                this.updateStartButton(this.assetRunning)
            }
        })

        openAssetsSelect.addEventListener("change", () => {
            const selectedAsset = this.getSelectedAsset()
            this.socket.emit("updateSelectedAsset", selectedAsset)
        })

        addAlertButton.addEventListener("click", () => {
            const alertPrice = priceAlertInput.value
            const selectedAsset = this.getSelectedAsset()
            this.socket.emit("alerts", {
                method: "POST",
                payload: {
                    asset_name: selectedAsset, 
                    price: alertPrice}
            })
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
        alertList.removeChild(alertItem)
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
    updateStartButton(running) {
        this.startButton.innerHTML = running 
        ? "<i class='ph ph-stop'></i> Parar" 
        : "<i class='ph ph-play'></i> Iniciar";
    }

    removeStartButton() {
        document.getElementById("assetHeader").removeChild(this.startButton)
        this.startButton = undefined
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
        if(this.getSelectedAsset() === name){
            assetName.innerText = name
        }
    }

    /**
     * @param {string} assetName 
     * @param {{id: number, date: string, message: string}[]} logs 
     */
    setLogs(assetName, logs) {
        if(this.getSelectedAsset() !== assetName){
            return
        }
        logList.querySelectorAll("li").forEach(li => logList.removeChild(li))
        logs.forEach(log => {
            logList.appendChild(logItem(log))
        })
    }

    setTransactions(transactions) {
        transactionList.querySelectorAll("li").forEach(li => transactionList.removeChild(li))
        transactions.forEach((transaction) => {
            transactionList.appendChild(transactionItem(transaction))
        })
    }

    /**
     * @param {string} assetName 
     * @param {{id: number, price: number}[]} alerts 
     */
    setAlerts(assetName, alerts) {
        if(this.getSelectedAsset() !== assetName){
            return
        }
        alertList.querySelectorAll("li").forEach(li => alertList.removeChild(li))
        alerts.forEach(alert => this.addAlertItem(alert))
    }

    /**
     * @param {string} assetName 
     * @param {number} price 
     */
    setPrice(assetName, price) {
        if(this.getSelectedAsset() === assetName){
            assetPrice.innerText = price || ""
        }
    }

    /**
     * @param {string} assetName 
     * @param {number} profit 
     */
    setProfit(assetName, profit) {
        if(this.getSelectedAsset() === assetName){
            assetProfit.innerText = `$ ${profit.toFixed(2)}`
        }
    }
    
    /**
     * @param {string} assetName 
     * @param {number} price 
     */
    setPriceAlertInput(assetName, price) { 
        if(this.getSelectedAsset() === assetName){
            priceAlertInput.value = price
        }
    }

    /**
     * @param {string} selectedAsset 
     * @param {string[]} openAssets 
     */
    setOpenAssets(selectedAsset, openAssets) {
        openAssets.forEach(asset => openAssetsSelect.appendChild(assetOption(asset)))
        openAssetsSelect.value = selectedAsset
    }
}

new HomePage()


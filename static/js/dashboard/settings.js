class SettingsPage {
    /**
     * @param {*} socket
     * @param {string} name 
     * @param {string} icon 
     * @param {boolean} active 
     */
    constructor(socket, name, icon, active) {
        this.socket = socket
        this.name = name
        this.icon = icon
        this.active = active
        
        this.socket.on("updateSetup", (data) => this.updateSetup(data))
    }

    
    getSelectedAccountMode() {
        let accountMode = "PRACTICE"
        document.getElementsByName("account_mode").forEach(input => {
            if(input.checked) {
                accountMode = input.defaultValue
            }
        })
        return accountMode
    }

    /** @param {string} accountMode */
    setSelectedAccountMode(accountMode) {
        document.getElementsByName("account_mode").forEach(input => {
            if(input.defaultValue == accountMode){
                input.checked = true
            }
        })
    }


    updateSetup(data) {
        this.setSelectedAccountMode(data.account_mode)
        document.getElementById("entryValueInput").value = data.money_amount
        document.getElementById("stopwinInput").value = data.stopwin
        document.getElementById("stoplossInput").value = data.stoploss
        document.getElementById("martingalesInput").value = data.martingales
        document.getElementById("sorosInput").value = data.soros
    }

    render() {
        document.getElementById("openAssets").classList.add("hidden")
        document.getElementById("page").innerHTML = this.getHTML()
        this.socket.emit(this.name, {"method": "GET", payload: {}})
    }

    getHTML() {
        return `
        <div class="settings-page">
            <form>
                <div class="input-wrapper">
                    <p>Conta</p>    
                    <label>
                        <input type="radio" name="account_mode" value="PRACTICE">
                        Treinamento
                    </label>
                </div>
                <div class="input-wrapper">
                    <label>
                        <input type="radio" name="account_mode" value="REAL">
                        Real
                    </label>
                </div>
                
                <label>
                    Valor da entrada
                    <input id="entryValueInput" type="number" value="1.0" step="0.1" required="true" min="1.0">
                </label>
                <span></span>
                <label>
                    Stop Win
                    <input id="stopwinInput" type="number" value="1.0" step="0.1" required="true" min="1.0">
                </label>
                <label>
                    Stop Loss
                    <input id="stoplossInput" type="number" value="1.0" step="0.1" required="true" min="1.0">
                </label>
                <label>
                    Martingales
                    <input id="martingalesInput" type="number" value="0" step="1" required="true" min="0">
                </label>
                <label>
                    Soros
                    <input id="sorosInput" type="number" value="0" step="1" required="true" min="0">
                </label>
            </form>
            <footer>
                <button id="saveButton">Salvar</button>
            </footer>
        </div>
        `
    }
}
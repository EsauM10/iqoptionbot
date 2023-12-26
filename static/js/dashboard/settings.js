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
        
        
    }

    render() {
        document.getElementById("openAssets").classList.add("hidden")
        document.getElementById("page").innerHTML = `
            <div class="settings-page">
                <form>
                    <div class="input-wrapper">
                        <p>Conta</p>    
                        <label>
                            <input type="radio" name="account-type" value="PRACTICE" checked="true">
                            Treinamento
                        </label>
                    </div>
                    <div class="input-wrapper">
                        <label>
                            <input type="radio" name="account-type" value="REAL">
                            Real
                        </label>
                    </div>
                    
                    <label>
                        Valor da entrada
                        <input type="number" value="1.0" step="0.1" required="true" min="1.0">
                    </label>
                    <span></span>
                    <label>
                        Stop Win
                        <input type="number" value="1.0" step="0.1" required="true" min="1.0">
                    </label>
                    <label>
                        Stop Loss
                        <input type="number" value="1.0" step="0.1" required="true" min="1.0">
                    </label>
                    <label>
                        Martingale
                        <input type="number" value="0" step="1" required="true" min="0">
                    </label>
                    <label>
                        Soros
                        <input type="number" value="0" step="1" required="true" min="0">
                    </label>
                </form>
            </div>
        `
    }
}
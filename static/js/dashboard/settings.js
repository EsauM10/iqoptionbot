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
                        <label>Conta</label>    
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
                    <div>
                        <label>Valor da entrada</label>
                        <input type="number" value="1.0" step="0.1" required="true" min="1.0">
                    </div>
                    <span></span>
                    <div>
                        <label>Stop Win</label>
                        <input type="number" value="1.0" step="0.1" required="true" min="1.0">
                    </div>
                    <div>
                        <label>Stop Loss</label>
                        <input type="number" value="1.0" step="0.1" required="true" min="1.0">
                    </div>
                    <div>
                        <label>Martingale</label>
                        <input type="number" value="0" step="1" required="true" min="0">
                    </div>
                    <div>
                        <label>Soros</label>
                        <input type="number" value="0" step="1" required="true" min="0">
                    </div>
                </form>
            </div>
        `
    }
}
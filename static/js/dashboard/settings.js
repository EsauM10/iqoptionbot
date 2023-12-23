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
        document.getElementById("page").innerHTML = `
            <div><h1>Settings</h1></div>
        `
    }
}
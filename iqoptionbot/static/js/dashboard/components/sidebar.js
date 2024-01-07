const menuList = document.getElementById("menuList")

class Sidebar {
    constructor(pages){
        pages.forEach(page => {
            menuList.appendChild(menuItem(page, () => {
                this.updateMenuList(page.name)
                page.render()
            }))
        })
    }

    /** @param {string} pageName */
    updateMenuList(pageName){
        menuList.querySelectorAll("li").forEach(li => {
            if(li.dataset.name === pageName){
                li.classList.add("active")
            }
            else {
                li.classList.remove("active")
            }
        })
    }
}
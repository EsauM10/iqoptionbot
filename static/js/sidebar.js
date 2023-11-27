const menuItems = document.querySelectorAll(".menuItem");

function setSelectedMenu() {
    menuItems.forEach((item) => {
        item.classList.remove("active");
        if(item.querySelector("a").pathname === window.location.pathname){
            item.classList.add("active");
        }
    })
}

setSelectedMenu()

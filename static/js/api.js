/** @param {string} pathname */
function redirect(pathname) {
    window.location.href = `${window.location.origin}/${pathname}`
}


/**
 * @param {string} email 
 * @param {string} password 
 * @returns {Promise<string>}
 */
async function login(email, password) {
    const url = `${window.location.origin}/login`
    const options = {
        method: "POST", 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, password})
    }
    const response = await fetch(url, options)
    const data = await response.json()

    if(!response.ok) {
        throw new Error(data.error)
    }

    return data.content
}

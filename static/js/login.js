window.onload = () => {
    const registerBtn = document.getElementById('registerBtn');
    
    if (registerBtn) {
        registerBtn.addEventListener('click', () => {
            console.log("Redirecting to /register");
            window.location.href = '/register'; 
        });
    } else {
        console.error("Register button not found!");
    }
};

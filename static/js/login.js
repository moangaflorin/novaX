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

document.getElementById("loginBtn").addEventListener("click", async function(event) {
    event.preventDefault(); 
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = "/chat";  
        } else {
            alert(data.detail);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while trying to log in. Please try again.");
    }
});

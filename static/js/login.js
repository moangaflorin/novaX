window.onload = () => {
    // Register button event listener
    const registerBtn = document.getElementById('registerBtn');
    if (registerBtn) {
        registerBtn.addEventListener('click', () => {
            console.log("Redirecting to /register");
            window.location.href = '/register'; 
        });
    } else {
        console.error("Register button not found!");
    }
    
    // Login button event listener
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener("click", async function(event) {
            event.preventDefault(); 
            
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("/login", {
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
    } else {
        console.error("Login button not found!");
    }
    
    // Forgot password button event listener
    const forgotPasswordBtn = document.getElementById('forgotPasswordBtn');
    if (forgotPasswordBtn) {
        forgotPasswordBtn.addEventListener('click', (event) => {
            event.preventDefault();
            console.log("Forgot password clicked");
            // Implement forgot password functionality here
            alert("Forgot password feature coming soon");
        });
    } else {
        console.error("Forgot password button not found!");
    }
};

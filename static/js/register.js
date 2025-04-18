document.getElementById("registerBtn").addEventListener("click", async function(event) {
    event.preventDefault(); 
    
    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;

    try {
        const response = await fetch("http://localhost:8000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                username: username,
                password: password,
                confirm_password: confirm_password,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = "/chat";  
        } else {
            alert(data.detail || "An unknown error occurred.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while trying to register. Please try again.");
    }
});

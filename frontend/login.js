document.addEventListener('DOMContentLoaded', function() {
    const API_URL = 'http://127.0.0.1:5000';
    const form = document.getElementById('authForm');

    if (form) {
        form.addEventListener('submit', async function(event) {
            event.preventDefault();
            console.log('Form submission prevented'); 
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorElement = document.getElementById('error-message');
            const submitBtn = document.querySelector('button[type="submit"]');
            
            submitBtn.disabled = true;
            console.log('Attempting login with:', username); 
            
            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });

                console.log('Response received:', response.status); 
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Login failed');
                }

                const data = await response.json();
                console.log('Login successful, token stored');
                localStorage.setItem('authToken', data.token);
                window.location.href = "/profile";
                
            } catch (error) {
                console.error('Login error:', error); 
                if (errorElement) {
                    errorElement.textContent = error.message;
                }
            } finally {
                submitBtn.disabled = false;
            }
        });
    } else {
        console.error('Form element not found!'); 
    }
});
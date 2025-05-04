const API_URL = 'http://127.0.0.1:5000'; 
console.log('Form submit handler called');
const authForm = document.getElementById('authForm')
authForm?.addEventListener('submit', async function(event) {
        event.preventDefault(); 
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('error-message')
    try {
        // Отправка данных на сервер
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

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('authToken', data.token);
            
            // Перенаправление через 1 секунду
            setTimeout(() => {
                window.location.href = "/profile";
            }, 1000);
        } else {
            // Ошибка авторизации\
            if (errorElement) {
                errorElement.textContent = data.error;
            }
            console.error('Login failed:', data);
        }
    } catch (error) {
        console.error('Error:', error);
        if (errorElement) {
            errorElement.textContent = "Ошибка соединения с сервером";
        }
    }
});
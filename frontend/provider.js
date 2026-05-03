document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    const validProviders = {
        provider1: "triage123",
        provider2: "triage456",
        provider3: "triage789"
    };

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        if (validProviders[username] && validProviders[username] === password) {
            sessionStorage.setItem('providerLoggedIn', true);
            sessionStorage.setItem('providerName', username);
            window.location.href = 'providerDashboard.html';
        } else {
            errorMessage.style.display = 'block';
        }
    });
});
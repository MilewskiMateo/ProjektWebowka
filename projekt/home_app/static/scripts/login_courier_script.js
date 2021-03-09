document.addEventListener('DOMContentLoaded', function (event) {
    
    const POST = "POST";
    const URL = "https://localhost:8083/login/log";
    
    let loginForm = document.getElementById("login-form");



    loginForm.addEventListener("submit", function (event) {
        event.preventDefault();
        submitLoginForm();
    }
    );
    
    function submitLoginForm() {
        let loginParams = {
            method: POST,
            credentials: 'include',
            body: new FormData(loginForm),
            
        };
    
        fetch(URL, loginParams)
            .then(response => { if (response.redirected) { window.location.href = response.url } else { return response.json() } })
            .then(response => { showResponse(response['responseMessage'],document.getElementById('submit-button'))})
            .catch(err => {
                console.log("Caught error: " + err);
            });
    }

    function showResponse(message,input){
        if (input.parentElement.getElementsByClassName('warning-message')[0] != null) {
            input.parentElement.removeChild(input.parentElement.getElementsByClassName('warning-message')[0]);
        }
        
        var errorLabel = document.createElement("label");

        errorLabel.appendChild(document.createTextNode(message));
        errorLabel.className = "warning-msg"
        errorLabel.id = "warning-message-id"
        input.parentElement.appendChild(errorLabel);
        
    }

    
})
document.addEventListener('DOMContentLoaded', function (event) {

    const GET = "GET";
    const POST = "POST";
    const URL_REGISTER = "https://localhost:8080/registration/register";
    const URL_LOGIN = "https://localhost:8080/checkLogin/";
    const LOGIN_FIELD_ID = "login";
    var EnableRegistration = false;
    var HTTP_STATUS = {OK: 200, CREATED: 201, NOT_FOUND: 404};

    //kolejnosci w liscie === login,pesel,haslo,haslo,loginzajety,imie,nazwisko,data,kraj,ulica,nr,kodpocztowy//
    var formValidationList = new Array(12);
    for (var i = 0; i < formValidationList.length; i++) { formValidationList[i] = false; }

    let registrationForm = document.getElementById("registration-form");
    let login = document.getElementById('login');

    const pesel = document.getElementById('pesel');
    const password = document.getElementById('password');
    const second_password = document.getElementById('second_password');
    const name = document.getElementById('name');
    const surname = document.getElementById('surname');
    const birth = document.getElementById('birth');
    const country = document.getElementById('country')
    const street = document.getElementById('street');
    const nr = document.getElementById('nr');
    const postal = document.getElementById('postal');
    prepareEventOnLoginChange();



    var formValidationProxy = new Proxy(formValidationList, {
        set: function (target, key, value) {
            target[key] = value;

            if (formValidationList.every((e) => (e))) {
                EnableRegistration = true;
                document.getElementById("button-reg-form").className = "submit-button-available";
            } else {
                EnableRegistration = false;
                document.getElementById("button-reg-form").className = "submit-button-not-available";
            }

            return true;
        }
    });


    registrationForm.addEventListener("submit", function (event) {
        event.preventDefault();
        if (EnableRegistration) {
            submitRegisterForm();
        }
    }
    );
    
    function submitRegisterForm() {
        let registerParams = {
            method: POST,
            body: new FormData(registrationForm),
        };
    
        fetch(URL_REGISTER, registerParams)
            .then(response => { if (response.redirected) { window.location.href = response.url } else { return response.json() } })
            .then(response => { setErrorFor(document.getElementById('button-reg-form'),response['responseMessage'])})
            .catch(err => {
                console.log("Caught error: " + err);
            });
    }

    /////////////////NADAWANIE LISTENEROW //////////////////////////

    name.addEventListener('change', (event) => {
        const nameValue = name.value.trim();
        if (nameValue === '') {
            setErrorFor(name, 'Imię jest puste');
            formValidationProxy[5] = false;
        } else if (!isName(nameValue)) {
            setErrorFor(name, 'Imię musi sie składać z samych liter');
            formValidationProxy[5] = false;
        } else {
            setSuccessFor(name);
            formValidationProxy[5] = true;
        }
    });

    surname.addEventListener('change', (event) => {
        const surnameValue = surname.value.trim();
        if (surnameValue === '') {
            setErrorFor(surname, 'Nazwisko jest puste');
            formValidationProxy[6] = false;
        } else if (!isName(surnameValue)) {
            setErrorFor(surname, 'Nazwisko musi sie składać z samych liter');
            formValidationProxy[6] = false;
        } else {
            setSuccessFor(surname);
            formValidationProxy[6] = true;
        }
    });

    birth.addEventListener('change', (event) => {
        const dateValue = birth.value.trim();
        if (dateValue === '') {
            setErrorFor(date, 'Data urodzenia jest pusta');
            formValidationProxy[7] = false;
        } else {
            setSuccessFor(birth);
            formValidationProxy[7] = true;
        }
    });

    country.addEventListener('change', (event) => {
        const countryValue = country.value.trim();
        if (countryValue === '') {
            setErrorFor(country, 'Kraj jest pusty');
            formValidationProxy[8] = false;
        } else if (!isName(countryValue)) {
            setErrorFor(country, 'Kraj musi sie składać z samych liter');
            formValidationProxy[8] = false;
        } else {
            setSuccessFor(country);
            formValidationProxy[8] = true;
        }
    });

    street.addEventListener('change', (event) => {
        const streetValue = street.value.trim();
        if (streetValue === '') {
            setErrorFor(street, 'Ulica jest pusta');
            formValidationProxy[9] = false;
        } else {
            setSuccessFor(street);
            formValidationProxy[9] = true;
        }
    });

    nr.addEventListener('change', (event) => {
        const nrValue = nr.value.trim();
        if (nrValue === '') {
            setErrorFor(nr, 'Numer zamieszkania jest pusty');
            formValidationProxy[10] = false;
        } else {
            setSuccessFor(nr);
            formValidationProxy[10] = true;
        }
    });

    postal.addEventListener('change', (event) => {
        const postalValue = postal.value.trim();
        if (postalValue === '') {
            setErrorFor(postal, 'Kod pocztowy jest pusty');
            formValidationProxy[11] = false;
        } else if (!isPostalCode(postalValue)) {
            setErrorFor(postal, 'Kod pocztowy musi mieć postać 00-000');
            formValidationProxy[11] = false;
        } else {
            setSuccessFor(postal);
            formValidationProxy[11] = true;
        }
    });

    login.addEventListener('change', (event) => {
        const loginValue = login.value.trim();
        if (loginValue === '') {
            setErrorFor(login, 'Login jest pusty');
            formValidationProxy[0] = false;
        } else if (!isLogin(loginValue)) {
            setErrorFor(login, 'Login musi się składać z minium 5 znaków będących małymi lub dużymi literami');
            formValidationProxy[0] = false;
        } else {
            setSuccessFor(login);
            formValidationProxy[0] = true;
        }
        if (registrationForm.getElementsByClassName("okStatusLabel")[0] != null) {
            registrationForm.removeChild(registrationForm.getElementsByClassName("okStatusLabel")[0]);
        }
    });

    pesel.addEventListener('change', (event) => {
        const peselValue = pesel.value.trim();
        if (peselValue === '') {
            setErrorFor(pesel, 'Pesel jest pusty');
            formValidationProxy[1] = false;
        } else if (!isPesel(peselValue)) {
            setErrorFor(pesel, 'Nieprawidłowy pesel');
            formValidationProxy[1] = false;
        } else {
            setSuccessFor(pesel);
            formValidationProxy[1] = true;

        }
    });


    password.addEventListener('change', (event) => {
        const passwordValue = password.value.trim();
        if (passwordValue === '') {
            setErrorFor(password, 'Hasło jest puste');
            formValidationProxy[2] = false;
        } else if (!isPassword(passwordValue)) {
            setErrorFor(password, 'Hasło musi zawierać conajmniej 8 znaków oraz zawierać mała literę, dużą literę, cyfrę i znak specjalny (!@#$%&*)');
            formValidationProxy[2] = false;
        } else {
            setSuccessFor(password);
            formValidationProxy[2] = true;
        }
    });
    second_password.addEventListener('change', (event) => {
        const second_passwordValue = second_password.value.trim();
        const passwordValue = password.value.trim();
        if (second_passwordValue === '') {
            setErrorFor(second_password, 'Hasło jest puste');
            formValidationProxy[3] = false;
        } else if (passwordValue !== second_passwordValue) {
            setErrorFor(second_password, 'Hasła się nie zgadzają');
            formValidationProxy[3] = false;
        } else {
            setSuccessFor(second_password);
            formValidationProxy[3] = true;
        }
    });
    //////////////////// Login Check//////////////////
    function prepareEventOnLoginChange() {
        let loginInput = document.getElementById(LOGIN_FIELD_ID);
        loginInput.addEventListener("change", updateLoginAvailabilityMessage);
    }

    function updateLoginAvailabilityMessage() {
        let warningElemId = "loginWarning";
        let warningMessage = "This login is already taken.";

        isLoginAvailable().then(function (isAvailable) {
            if (isAvailable) {
                console.log("Available login!");
                removeLoginWarningMessage(warningElemId);
                login.className= "row-is-valid";
                 formValidationProxy[4]=true;
            } else {
                console.log("NOT available login");
                showLoginWarningMessage(warningElemId, warningMessage);
                login.className= "row-is-invalid";
                formValidationProxy[4]=false;
            }
        }).catch(function (error) {
            console.error("Something went wrong while checking login.");
            console.error(error);
        });
    }

    function showLoginWarningMessage(newElemId, message) {
        let warningElem = prepareLoginWarningElem(newElemId, message);
        appendAfterElem(LOGIN_FIELD_ID, warningElem);
    }

    function removeLoginWarningMessage(warningElemId) {
        let warningElem = document.getElementById(warningElemId);

        if (warningElem !== null) {
            warningElem.remove();
        }
    }

    function prepareLoginWarningElem(newElemId, message) {
        let warningField = document.getElementById(newElemId);

        if (warningField === null) {
            let textMessage = document.createTextNode(message);
            warningField = document.createElement('span');

            warningField.setAttribute("id", newElemId);
            warningField.className = "warning-field";
            warningField.appendChild(textMessage);
        }
        return warningField;
    }

    function appendAfterElem(currentElemId, newElem) {
        let currentElem = document.getElementById(currentElemId);
        currentElem.insertAdjacentElement('afterend', newElem);
    }

    function isLoginAvailable() {
        return Promise.resolve(checkLoginAvailability().then(function (statusCode) {
            console.log(statusCode);
            if (statusCode === HTTP_STATUS.OK) {
                return false;

            } else if (statusCode === HTTP_STATUS.NOT_FOUND) {
                return true

            } else {
                throw "Unknown login availability status: " + statusCode;
            }
        }));
    }

    function checkLoginAvailability() {
        let loginInput = document.getElementById(LOGIN_FIELD_ID);
        let userUrl = URL_LOGIN + loginInput.value;

        return Promise.resolve(fetch(userUrl, {method: GET}).then(function (resp) {
            
            return resp.status;
        }).catch(function (err) {
            return err.status;
        }));
    }




    /////////////////POMOCNICZE///////////////////////

    function setErrorFor(input, message) {
        if (input.parentElement.getElementsByClassName('warning-message')[0] != null) {
            input.parentElement.removeChild(input.parentElement.getElementsByClassName('warning-message')[0]);
        }
        var errorLabel = document.createElement("label");

        errorLabel.appendChild(document.createTextNode(message));
        errorLabel.className = "warning-message"
        errorLabel.id = "warning-message-id"
        input.parentElement.appendChild(errorLabel);


        input.className = "row-is-invalid";
    }

    function setSuccessFor(input) {
        if (input.parentElement.getElementsByClassName('warning-message')[0] != null) {
            input.parentElement.removeChild(input.parentElement.getElementsByClassName('warning-message')[0]);
        }
        input.className = "row-is-valid";
    }

    function isLogin(login) {
        return /^[a-zA-Z]{5,}$/.test(login);
    }
    function isPassword(password) {
        return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(password);
    }
    function isPostalCode(postal) {
        return /^[0-9]{2}-[0-9]{3}$/.test(postal)
    }
    function isName(name) {
        return /^.*[a-zA-Z]$/.test(name)
    }

    function isPesel(pesel) {
        if (/^[0-9]{11}$/.test(pesel) == false)
            return false;
        else {
            var digits = ("" + pesel).split("");
            var checksum = (1 * parseInt(digits[0]) + 3 * parseInt(digits[1]) + 7 * parseInt(digits[2]) + 9 * parseInt(digits[3]) + 1 * parseInt(digits[4]) + 3 * parseInt(digits[5]) + 7 * parseInt(digits[6]) + 9 * parseInt(digits[7]) + 1 * parseInt(digits[8]) + 3 * parseInt(digits[9])) % 10;
            if (checksum == 0) { checksum = 10; }
            else {
                checksum = 10 - checksum;
            }
            return (parseInt(digits[10]) == checksum);
        }
    }
});
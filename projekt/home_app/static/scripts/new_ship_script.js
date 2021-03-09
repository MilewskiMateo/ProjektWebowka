document.addEventListener('DOMContentLoaded', function (event) {
    
    const GET = "GET";
    const POST = "POST";
    const URL = "https://localhost:8080/new_ship/add";
    const LOGIN_FIELD_ID = "login";
    
    //kolejnosci w liscie === name,surname,country,street,nr,postal,tel//
    var formValidationList = new Array(14);
    for (var i = 0; i < formValidationList.length; i++) { formValidationList[i] = false; }
    
    var EnableRegistration = false;
    
    let newShipForm = document.getElementById('new-ship-form');
    const name = document.getElementById('name');
    const surname = document.getElementById('surname');
    const country = document.getElementById('country')
    const street = document.getElementById('street');
    const nr = document.getElementById('nr');
    const postal = document.getElementById('postal');
    const telephone = document.getElementById('telephone');
    const sender_name = document.getElementById('sender_name');
    const sender_surname = document.getElementById('sender_surname');
    const sender_country = document.getElementById('sender_country')
    const sender_street = document.getElementById('sender_street');
    const sender_nr = document.getElementById('sender_nr');
    const sender_postal = document.getElementById('sender_postal');
    const sender_telephone = document.getElementById('sender_telephone');
    
    
    
    
    
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
    
    newShipForm.addEventListener("submit", function (event) {
        event.preventDefault();
        if (EnableRegistration) {
            submitNewShipForm();
            clearForm();
            for (var i = 0; i < formValidationList.length; i++) { formValidationList[i] = false; }
            EnableRegistration = false;
        }
    }
    );
    
    function submitNewShipForm() {
        console.log(URL)
        let fetchParams = {
            method: POST,
            body: new FormData(newShipForm),
        };
    
        fetch(URL, fetchParams)
            .then(response => { if (response.redirected) { window.location.href = response.url } else { return response.json() } })
            .then(response => { setSuccesForShipAdd(document.getElementById('button-reg-form'))})
            .catch(err => {
                console.log("Caught error: " + err);
            });
    }

    /////////////////NADAWANIE LISTENEROW  1    //////////////////////////

    name.addEventListener('change', (event) => {
        const nameValue = name.value.trim();
        if (nameValue === '') {
            setErrorFor(name, 'Imię jest puste');
            formValidationProxy[0] = false;
        } else if (!isName(nameValue)) {
            setErrorFor(name, 'Imię musi sie składać z samych liter');
            formValidationProxy[0] = false;
        } else {
            setSuccessFor(name);
            formValidationProxy[0] = true;
        }
    });

    surname.addEventListener('change', (event) => {
        const surnameValue = surname.value.trim();
        if (surnameValue === '') {
            setErrorFor(surname, 'Nazwisko jest puste');
            formValidationProxy[1] = false;
        } else if (!isName(surnameValue)) {
            setErrorFor(surname, 'Nazwisko musi sie składać z samych liter');
            formValidationProxy[1] = false;
        } else {
            setSuccessFor(surname);
            formValidationProxy[1] = true;
        }
    });

    country.addEventListener('change', (event) => {
        const countryValue = country.value.trim();
        if (countryValue === '') {
            setErrorFor(country, 'Kraj jest pusty');
            formValidationProxy[2] = false;
        } else if (!isName(countryValue)) {
            setErrorFor(country, 'Kraj musi sie składać z samych liter');
            formValidationProxy[2] = false;
        } else {
            setSuccessFor(country);
            formValidationProxy[2] = true;
        }
    });

    street.addEventListener('change', (event) => {
        const streetValue = street.value.trim();
        if (streetValue === '') {
            setErrorFor(street, 'Ulica jest pusta');
            formValidationProxy[3] = false;
        } else {
            setSuccessFor(street);
            formValidationProxy[3] = true;
        }
    });

    nr.addEventListener('change', (event) => {
        const nrValue = nr.value.trim();
        if (nrValue === '') {
            setErrorFor(nr, 'Numer zamieszkania jest pusty');
            formValidationProxy[4] = false;
        } else {
            setSuccessFor(nr);
            formValidationProxy[4] = true;
        }
    });

    postal.addEventListener('change', (event) => {
        const postalValue = postal.value.trim();
        if (postalValue === '') {
            setErrorFor(postal, 'Kod pocztowy jest pusty');
            formValidationProxy[5] = false;
        } else if (!isPostalCode(postalValue)) {
            setErrorFor(postal, 'Kod pocztowy musi mieć postać 00-000');
            formValidationProxy[5] = false;
        } else {
            setSuccessFor(postal);
            formValidationProxy[5] = true;
        }
    });

    
    telephone.addEventListener('change', (event) => {
        const telephoneValue = telephone.value.trim();
        if (telephoneValue === '') {
            setErrorFor(telephone, 'Numer kontaktowy jest pusty');
            formValidationProxy[6] = false;
        } else if (!isTelephone(telephoneValue)) {
            setErrorFor(telephone, 'Numer kontaktowy musi składać się z 9 cyfr bez kodu kierunkowego');
            formValidationProxy[6] = false;
        } else {
            setSuccessFor(telephone);
            formValidationProxy[6] = true;
        }
    });



    /////////////////NADAWANIE LISTENEROW  2  //////////////////////////





    sender_name.addEventListener('change', (event) => {
            const nameValue = sender_name.value.trim();
            if (nameValue === '') {
                setErrorFor(sender_name, 'Imię jest puste');
                formValidationProxy[7] = false;
            } else if (!isName(nameValue)) {
                setErrorFor(sender_name, 'Imię musi sie składać z samych liter');
                formValidationProxy[7] = false;
            } else {
                setSuccessFor(sender_name);
                formValidationProxy[7] = true;
            }
        });

    sender_surname.addEventListener('change', (event) => {
        const surnameValue = sender_surname.value.trim();
        if (surnameValue === '') {
            setErrorFor(sender_surname, 'Nazwisko jest puste');
            formValidationProxy[8] = false;
        } else if (!isName(surnameValue)) {
            setErrorFor(sender_surname, 'Nazwisko musi sie składać z samych liter');
            formValidationProxy[8] = false;
        } else {
            setSuccessFor(sender_surname);
            formValidationProxy[8] = true;
        }
    });

    sender_country.addEventListener('change', (event) => {
        const countryValue = sender_country.value.trim();
        if (countryValue === '') {
            setErrorFor(sender_country, 'Kraj jest pusty');
            formValidationProxy[9] = false;
        } else if (!isName(countryValue)) {
            setErrorFor(sender_country, 'Kraj musi sie składać z samych liter');
            formValidationProxy[9] = false;
        } else {
            setSuccessFor(sender_country);
            formValidationProxy[9] = true;
        }
    });

    sender_street.addEventListener('change', (event) => {
        const streetValue = sender_street.value.trim();
        if (streetValue === '') {
            setErrorFor(sender_street, 'Ulica jest pusta');
            formValidationProxy[10] = false;
        } else {
            setSuccessFor(sender_street);
            formValidationProxy[10] = true;
        }
    });

    sender_nr.addEventListener('change', (event) => {
        const nrValue = sender_nr.value.trim();
        if (nrValue === '') {
            setErrorFor(sender_nr, 'Numer zamieszkania jest pusty');
            formValidationProxy[11] = false;
        } else {
            setSuccessFor(sender_nr);
            formValidationProxy[11] = true;
        }
    });

    sender_postal.addEventListener('change', (event) => {
        const postalValue = sender_postal.value.trim();
        if (postalValue === '') {
            setErrorFor(sender_postal, 'Kod pocztowy jest pusty');
            formValidationProxy[12] = false;
        } else if (!isPostalCode(postalValue)) {
            setErrorFor(sender_postal, 'Kod pocztowy musi mieć postać 00-000');
            formValidationProxy[12] = false;
        } else {
            setSuccessFor(sender_postal);
            formValidationProxy[12] = true;
        }
    });

    
    sender_telephone.addEventListener('change', (event) => {
        const telephoneValue = sender_telephone.value.trim();
        if (telephoneValue === '') {
            setErrorFor(sender_telephone, 'Numer kontaktowy jest pusty');
            formValidationProxy[13] = false;
        } else if (!isTelephone(telephoneValue)) {
            setErrorFor(sender_telephone, 'Numer kontaktowy musi składać się z 9 cyfr bez kodu kierunkowego');
            formValidationProxy[13] = false;
        } else {
            setSuccessFor(sender_telephone);
            formValidationProxy[13] = true;
        }
    });


    /////////////////   Pomocnicze   //////////////////////////


    function setErrorFor(input, message) {
        if (input.parentElement.getElementsByClassName('warning-message')[0] != null) {
            input.parentElement.removeChild(input.parentElement.getElementsByClassName('warning-message')[0]);
        }
        var errorLabel = document.createElement("label");

        errorLabel.appendChild(document.createTextNode(message));
        errorLabel.className = "warning-message"
        errorLabel.id = "warning-message-id"
        input.parentElement.appendChild(errorLabel);
        

       if(input.type==='text'){ input.className = "row-is-invalid"};
    }

    function setSuccessFor(input) {
        if (input.parentElement.getElementsByClassName('warning-message')[0] != null) {
            input.parentElement.removeChild(input.parentElement.getElementsByClassName('warning-message')[0]);
        }
        input.className = "row-is-valid";
    }
    function setSuccesForShipAdd(input){
        if (input.parentElement.getElementsByClassName('succes-message')[0] != null) {
            input.parentElement.removeChild(input.parentElement.getElementsByClassName('succes-message')[0]);
        }
        var errorLabel = document.createElement("label");

        errorLabel.appendChild(document.createTextNode("Dodano paczkę"));
        errorLabel.className = "succes-message"
        errorLabel.id = "succes-message-id"
        input.parentElement.appendChild(errorLabel);
    }

    function isPostalCode(postal) {
        return /^[0-9]{2}-[0-9]{3}$/.test(postal)
    }
    function isName(name) {
        return /^.*[a-zA-Z]$/.test(name)
    }
    function isTelephone(tele){
       return /^(?:\(?\?)?(?:[-\.\(\)\s]*(\d)){9}\)?$/.test(tele)
    }
    function clearForm(){
        name.value="";
        surname.value="";
        country.value="";
        street .value="";
        nr.value="";
        postal.value="";
        telephone.value="";
        sender_name.value="";
        sender_surname.value="";
        sender_country.value="";
        sender_street.value="";
        sender_nr.value="";
        sender_postal.value="";
        sender_telephone.value="";
    }
})
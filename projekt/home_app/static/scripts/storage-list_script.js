document.addEventListener('DOMContentLoaded', function (event) {
    
    const POST = "POST";
    const URL = "https://localhost:8082/storage/pick";
    
    let pickForm = document.getElementById("storage-list-form");
    let courierId = document.getElementById("courier-id");
    let lockerId = document.getElementById("locker-id");
    
    makeListeners()


    pickForm.addEventListener("submit", function (event) {
        event.preventDefault();
        submitForm();
    }
    );
    
    function submitForm() {
        myFormData= prepreFormData()
        let loginParams = {
            method: POST,
            body: myFormData,
            
        };
    
        fetch(URL, loginParams)
            .then(response => { if (response.redirected) { window.location.href = response.url } else { return response.json() } })
            .then(response => {console.log(response) })
            .catch(err => {
                console.log("Caught error: " + err);
            });
    }
    function prepreFormData(){
        var myBody = new FormData()
        myBody.append('courier_id',courierId.value)
        myBody.append('locker_id',lockerId.value)

        Object.keys(localStorage).forEach(function(key){
            myBody.append('checkboxes',key)
         });
        return myBody
    }


    function makeListeners(){
        var checkboxes = document.getElementsByName('checkbox');
        checkboxes.forEach(element => {
            if (localStorage.getItem(element.value) === 'True') {
                element.checked = true
              }
            element.addEventListener("change", function (event) {
              if(localStorage.getItem(element.value) === null){
                  localStorage.setItem(element.value,'True');
                }else{
                  localStorage.removeItem(element.value);             
              }
            }
            );
        });
    }

    
})
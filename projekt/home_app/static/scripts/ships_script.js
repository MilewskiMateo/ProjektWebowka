document.addEventListener('DOMContentLoaded', function (event) {
    
    let deleteButtonsA = document.getElementsByClassName('delete-button');
    

    for (let i = 0; i < deleteButtonsA.length; i++) {
        deleteAnchor =  deleteButtonsA[i].parentElement;
        url =  deleteAnchor.href
        deleteAnchor.addEventListener("click",function(event){
            event.preventDefault();
            deleteShip(url);
        })
        
    }

    
    function deleteShip(url) {
        console.log("delete")
        fetch(url, {method: "DELETE"})
            .then(response => { if (response.redirected) { window.location.href = response.url } else { return response.json() } })
            .catch(err => {
                console.log("Caught error: " + err);
            });
    }

})
document.addEventListener('DOMContentLoaded', function (event) {

   
    var rowList = document.getElementById("laureates_tbody").getElementsByTagName("tr");
  
    for (index = 0; index < rowList.length; ++index) {
 
        (function(x){
            rowList[x].addEventListener("mouseover",e => {
                if(x%2==0){
                rowList[x].className="yellowRow";
                }else{
                rowList[x].className="redRow";    
                }
            });
        })(index)
    }

    for (index = 0; index < rowList.length; ++index) {

        (function(y){
            rowList[y].addEventListener("mouseout",e => {
                if(y%2==0){
                    rowList[y].className="greenRow";
                }else{
                rowList[y].className="blueRow";    
                }
            });
        })(index)
    }
});
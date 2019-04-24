$(document).ready(function () {
    var alltypebtn =document.getElementById("alltypebtn")
    var showsortbtn =document.getElementById("showsortbtn")

    var typediv =document.getElementById("typediv")
    var sortdiv =document.getElementById("sortdiv")
    var addShoppingbtn=document.getElementsByClassName("addShopping")
    var subShoppingbtn=document.getElementsByClassName("subShopping")
    typediv.style.display="none"
    sortdiv.style.display="none"

    alltypebtn.addEventListener("click",function () {
        typediv.style.display="block"
        sortdiv.style.display="none"
    },false)

    showsortbtn.addEventListener("click",function () {
        typediv.style.display="none"
        sortdiv.style.display="block"
    },false)
    typediv.addEventListener("click",function () {
        typediv.style.display="none"

    },false)
    sortdiv.addEventListener("click",function () {
        sortdiv.style.display="none"
    },false)
    for (var i=0;i<addShoppingbtn.length;i++){
        addShoppingbtn[i].addEventListener("click",function () {
            pid= this.getAttribute("ga")
            $.post("/changecart/0/",{"productid":pid},function(data){

                if (data.status=="success"){
                    document.getElementById(pid).innerHTML=data.data
                }
                else {
                    if (data.data=='-1'){
                        window.location.href="http://127.0.0.1:8000/login/"
                    }
                }
            })
    },false)}
    for (var i=0;i<subShoppingbtn.length;i++){
        subShoppingbtn[i].addEventListener("click",function () {
            pid= this.getAttribute("ga")
            $.post("/changecart/1/",{"productid":pid},function(data){

                if (data.status=="success"){
                    document.getElementById(pid).innerHTML=data.data
                }
                else {
                    if (data.data=='-1'){
                        window.location.href="http://127.0.0.1:8000/login/"
                    }
                }
            })
    },false)}

})
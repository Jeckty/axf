$(document).ready(function () {
    var ischooses =document.getElementsByClassName("ischose")
    for (var i=1;i<ischooses.length;i++){

        ischoose=ischooses[i]
        ischoose.addEventListener("click",function () {
            pid=this.getAttribute("goodsid")
            $.post("/changecart/3/",{"productid":pid},function (data) {
                    if (data.status == "success"){
                    //window.location.href = "http://127.0.0.1:8001/cart/"
                    var s = document.getElementById(pid+"a")
                    s.innerHTML = data.data
                }
                })
            })
        }
    })

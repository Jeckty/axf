$(document).ready(function () {
    var ischooses =document.getElementsByClassName("ischose")
    var addShoppingbtn=document.getElementsByClassName("addShopping")
    var subShoppingbtn=document.getElementsByClassName("subShopping")
    var confirmbtn=document.getElementById("con2")
    var okbtn=document.getElementById("ok")
    for (var i=0;i<ischooses.length;i++){

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
                    if (data.data==0){
                        document.getElementById(pid+"li").style.display=("None")
                    }
                }
                else {
                    if (data.data=='-1'){
                        window.location.href="http://127.0.0.1:8000/login/"
                    }
                }
            })
    },false)}
    // 全选
    confirmbtn.addEventListener("click",function () {

        if (this.innerHTML=="√"){
            this.innerHTML='0'
        }
        else{
            // alert("hhhhh")
            this.innerHTML="√"
            $.post("/changecart/4/",function(data){
            if (data.status=="success"){
                ischoses2s=document.getElementsByClassName("ischose2")
                // document.getElementById("con2").innerHTML=data.data
                for (var i=0;i<ischoses2s.length;i++){
                    ischoses2s[i].innerHTML=data.data
                }
            }
            })
        }})

    // 选好了
    okbtn.addEventListener("click",function () {
        $.post("/changecart/5/",function (data) {
            // for (i=0;i<data.productList.length;i++)
                // document.getElementById(data.productList[i]+"li").style.display="None"
            window.location.reload()
            alert("您的订单已生成，订单号："+data.data)
        })
    })

    })

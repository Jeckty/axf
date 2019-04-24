from django.shortcuts import render,redirect
from django.http import JsonResponse
import time,random
from .models import Wheel,nav,Mustbuy,Shop,MainShow,FoodTypes,Goods,User,Cart
from django.conf import settings
import os
from django.contrib.auth import logout

# Create your views here.
def home(request):
    wheelsList=Wheel.objects.all()
    navList=nav.objects.all()
    mustbuyList=Mustbuy.objects.all()
    shopList=Shop.objects.all()
    shop1=shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]
    mainList=MainShow.objects.all()

    return render(request, 'axf/home.html',{"title":"主页","wheelsList":wheelsList,"navList":navList,"mustbuyList":mustbuyList,"shop1":shop1,"shop2":shop2,"shop3":shop3,"shop4":shop4,"mainList":mainList})

def market(request,categoryid,cid,sortid):
    leftSlider=FoodTypes.objects.all()
    if cid == '0':
        productList=Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid,childcid=cid)
    group=leftSlider.get(typeid=categoryid)
    childList=[]
    childnames=group.childtypenames
    arr1=childnames.split("#")
    for str in arr1:
        arr2=str.split(":")
        obj={"childName":arr2[0],"childId":arr2[1]}
        childList.append(obj)
    if sortid=="1":
        productList=productList.order_by("productnum")
    elif sortid=="2":
        pass
    elif sortid=="3":
        pass
    return render(request, "axf/market.html",{"title":"闪送超市","leftSlider":leftSlider,"productList":productList,"childList":childList,"categoryid":categoryid,"cid":cid})

def cart(request):
    return render(request,'axf/cart.html',{"title":"购物车"})

def mine(request):
    username=request.session.get("username","未登录")
    return render(request,'axf/mine.html',{"title":"我的","username":username})
#注册
def register(request):
    if request.method=="POST":
        userAccount = request.POST.get("userAccount")
        userPasswd  = request.POST.get("userPasswd")
        userName    = request.POST.get("userName")
        userPhone   = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank    = 0
        Token=time.time() + random.randrange(1, 100000)
        userToken   =str(Token)
        f=request.FILES["userImg"]
        userImg=os.path.join(settings.MDEIA_ROOT,userAccount+".png")
        with open (userImg,"wb") as fp:
            for date in f.chunks():
                fp.write(date)

        user=User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()
        request.session["username"] = userName
        request.session["token"] = userToken
        return redirect("/mine/")
    else:
        return render(request,'axf/register.html',)

#检查用户明是否可用
def checkuserid(request):
    userid=request.POST.get("userid")
    try:
        user=User.objects.get(userAccount=userid)
        return JsonResponse({"data":"改用户已经被注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"可以注册","status":"success"})

#退出登陆
def quit(request):
    logout(request)
    return redirect("/mine/")

#登陆
from .forms.login import LoginForm
from django.http import HttpResponse
def login(request):
    if request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():
            # 信息格式没多大问题，验证账号和密码的正确性
            nameid = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            try:
                user = User.objects.get(userAccount = nameid)
                if user.userPasswd != pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                return redirect('/login/')

            #登陆成功
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session["username"] = user.userName
            request.session["token"] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'axf/login.html', {"title": "登陆", "form": f,"error":f.errors})
    else:
        f = LoginForm()
        return render(request, 'axf/login.html', {"title": "登陆","form":f})

def changecart(request,flag):
    #检查是否登陆
    usertoken =request.session.get("token")
    if usertoken==None:
        return JsonResponse({"data":"-1","status":"error"})
    user = User.objects.get(userToken=usertoken)
    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    if flag=='0':
        if product.storenums ==0:
            return JsonResponse({"data":"-2","status":"error"})
        carts=Cart.objects.filter(userAccount=user.userAccount)
        c=None
        if carts.count()==0:
            c=Cart.createcart(user.userAccount,productid,1,product.price,True,product.productimg,product.productlongname,False)
            c.save()
        else:
            try:
                c=carts.get(productid=productid)
                c.productnum+=1
                c.productprice = "%.2f" % (float(product.price) * c.productnum)
                c.save()
            except Cart.DoesNotExist as e:
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,product.productlongname, False)
                c.save()
        product.storenums-=1
        product.save()
        print(c.productnum)
        return JsonResponse({"data":c.productnum, "price":c.productprice,"status":"success"})
    if flag=='1':

        carts=Cart.objects.filter(userAccount=user.userAccount)
        try:
            c=carts.get(productid=productid)
            c.productnum -= 1
            if c.productnum == 0:
                c.delete()
            else:
                c.productprice = "%.2f" % (float(product.price) * c.productnum)
                c.save()
                product.storenums += 1
                product.save()
                return JsonResponse({"data": c.productnum, "price": c.productprice, "status": "success"})
        except Cart.DoesNotExist as e:
            return JsonResponse({"data": "-2", "status": "error"})



        product.storenums+=1
        product.save()
        print(c.productnum)
        return JsonResponse({"data":c.productnum, "price":c.productprice,"status":"success"})




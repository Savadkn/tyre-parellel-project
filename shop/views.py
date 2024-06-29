from django.shortcuts import render,redirect

# Create your views here.

from shop.forms import SignUpForm,SignInForm

from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from shop.models import Product,Basket,BasketItem,Size,Order

class RegistrationView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            # User.objects.create_user(**data)

            print("account created")

            return redirect("register")

        return render(request,"register.html",{"form":form_instance})

class LoginView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,"signin.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

        if user_object:

            login(request,user_object)

            print("session started")

            return redirect("index")
        
        print("failed to login")

        return render(request,"signin.html",{"form":form_instance})
    
class IndexView(View):

    def get(self,request,*args,**kwargs):

        qs=Product.objects.all()

        return render(request,"index.html",{"data":qs})

class ProductDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Product.objects.get(id=id)

        return render(request,"product_detail.html",{"data":qs})
    
class AddToCartView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        basket_obj=request.user.cart

        product_obj=Product.objects.get(id=id)

        size_name=request.POST.get("size")

        size_obj=Size.objects.get(name=size_name)

        qty=request.POST.get("qty")

        basket_item_obj=BasketItem.objects.filter(basket_object=basket_obj,product_object=product_obj,size_object=size_obj,is_order_placed=False)

        if basket_item_obj:

            basket_item_obj[0].quantity+=int(qty)

            basket_item_obj[0].save()

        else:

            BasketItem.objects.create(
                basket_object=basket_obj,
                product_object=product_obj,
                size_object=size_obj,
                quantity=qty

        )

        print("item added to cart")

        return redirect("index")


class CartSummaryView(View):

    def get(self,request,*args,**kwargs):



        qs=request.user.cart.cartitems.filter(is_order_placed=False)

        return render(request,"cart_list.html",{"data":qs})
    
class CartDestroyView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        BasketItem.objects.get(id=id).delete()

        return redirect("cart-summary")

class SignoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    
class CartQuantityUpdateView(View):

    def post(self,request,*args,**kwargs):

        action=request.POST.get("action")

        id=kwargs.get("pk")

        basket_item_obj=BasketItem.objects.get(id=id)

        if action == "increment":

            basket_item_obj.quantity+=1
        else:
            basket_item_obj.quantity-=1
        
        basket_item_obj.save()

        return redirect("cart-summary")
    
class PlaceOrderView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"place_order.html")
    
    def post(self,request,*args,**kwargs):

        email=request.POST.get("email")

        phone=request.POST.get("phone")

        address=request.POST.get("address")

        payment_mode=request.POST.get("payment_mode")

        pin=request.POST.get("pin")

        print(email,phone,address,payment_mode,pin)

        user_obj=request.user
        
        basket_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)
        
        if payment_mode== "cod":

            print("in")

            order_obj=Order.objects.create(

                user_object=user_obj,
                delivery_address=address,
                phone=phone,
                email=email,
                payment_mode=payment_mode,
                pin=pin,
               
                
            )

            for bi in basket_item_objects:

                order_obj.basket_item_objects.add(bi)

                bi.is_order_placed=True

                bi.save()

                order_obj.save()

        

        return redirect("index")



class OrderSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(user_object=request.user).order_by

        return render(request,"order_summary.html",{"data":qs})
    
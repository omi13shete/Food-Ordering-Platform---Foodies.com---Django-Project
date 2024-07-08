from django.shortcuts import render
from restaurant.models import DishCart,RestaurantRegistration,Order,OrderDish
from customer.models import Customer_Profile
from django.http import JsonResponse
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from .paypal_client import PayPalClient
from django.views.decorators.csrf import csrf_exempt
from .paypal_client import paypal_client
import razorpay
from Food_Platform.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Q




client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
def customer_checkout(request):
    if request.user.is_authenticated:
        print(request.user)
        cart_data=DishCart.objects.filter(user=request.user)
        print(cart_data)
        customer_details=Customer_Profile.objects.get(User=request.user)
        print(customer_details)
        amount=0
        total_price=0
        cart_items=DishCart.objects.filter(user=request.user)
        for p in cart_items:
            amount=(p.quantity*p.dish.Dis_price)
            total_price += amount
    order_price=total_price*100
    print(order_price)
    DATA = {
    "amount": order_price,
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
}
    api_key=RAZORPAY_API_KEY

    order=client.order.create(data=DATA)
    print(order)
    order_id=order["id"]
    return render(request,"payment/checkout.html",{"api_key":api_key,"order_id":order_id,"order_price":order_price,"customer_details":customer_details,"cart_data":cart_data,'total_price':total_price})


# def order_created(request):
#     cart_data=DishCart.objects.filter(user=request.user)
#     amount=0
#     pay_price=0
#     amount=0
#     total_price=0
#     cart_items=DishCart.objects.filter(user=request.user)
#     for p in cart_items:
#         amount=(p.quantity*p.dish.Dis_price)
#         total_price += amount
#         print(total_price)
#     for p in cart_data:
#         amount=(p.quantity*p.dish.Dis_price)
#         pay_price += amount
#         restaurant=p.dish.restaurant.restaurant_name
#         order_restaurant_name=RestaurantRegistration.objects.get(restaurant_name=restaurant)
#         print(order_restaurant_name)
#         dishes_list=[]
#         dish=p.dish
#         dishes_list.append(dish)
#         print(dishes_list)
#         order=Order(user=request.user,total_price=amount,restaurant=order_restaurant_name)
#         order.save()
#         if dishes_list:
#             order.dishes.set(dishes_list)
#         p.delete()
    
#     my_order=Order.objects.filter(user=request.user).latest("created_at")
#     print("my order is :",my_order)
#     print(my_order.id)
#     dishes=OrderDish.objects.filter(order=my_order)
#     customer_details=Customer_Profile.objects.get(User=request.user)
#     order_data=Order.objects.filter(Q(user=request.user))
#     # print(order_data)
#     order_confirmation_email(request)
#     return render(request,"payment/order.html",{"order_data":order_data,"customer_details":customer_details,"dishes_list":dishes,"total_bill":total_price})



from django.db import transaction

def order_created(request):
    cart_items = DishCart.objects.filter(user=request.user)

    total_price = 0
    dishes_list = []

    for cart_item in cart_items:
        amount = cart_item.quantity * cart_item.dish.Dis_price
        total_price += amount
        dishes_list.append(cart_item.dish)

    with transaction.atomic():
        first_item=cart_items.first()
        restaurant=first_item.dish.restaurant.restaurant_name
        order_restaurant_name = RestaurantRegistration.objects.get(restaurant_name=restaurant)
        order = Order.objects.create(user=request.user, total_price=total_price, restaurant=order_restaurant_name)
        
        if dishes_list:
            order.dishes.set(dishes_list)
        
        cart_items.delete()

    my_order = Order.objects.filter(user=request.user).latest("created_at")
    dishes = OrderDish.objects.filter(order=my_order)
    customer_details = Customer_Profile.objects.get(User=request.user)
    order_data = Order.objects.filter(user=request.user, id=my_order.id)
    print(order_data)
    order_confirmation_email(request)
    return render(request, "payment/order.html", {
        "order_data": order_data,
        "customer_details": customer_details,
        "dishes_list": dishes,
    })

@csrf_exempt
def create_order(request):
    paypal_client = PayPalClient()
    total_price=0
    cart_items=DishCart.objects.filter(user=request.user)
    for p in cart_items:
        amount=(p.quantity*p.dish.Dis_price)
        total_price += amount
    print(total_price)
    request_order = OrdersCreateRequest()
    request_order.prefer('return=representation')
    request_order.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": total_price  # Replace with dynamic value if necessary
            }
        }]
    })

    response = paypal_client.client.execute(request_order)
    return JsonResponse({'id': response.result.id})


@csrf_exempt
def capture_order(request, order_id):
    if request.method == 'POST':
        try:
            capture_request = OrdersCaptureRequest(order_id)
            capture_request.prefer('return=representation')
            
            response = paypal_client.execute(capture_request)
            print(response)  # Log the response for debugging
            
            capture_id = response.result.purchase_units[0].payments.captures[0].id
            capture_status = response.result.purchase_units[0].payments.captures[0].status
            
            return JsonResponse({'status': capture_status, 'id': capture_id})
        except Exception as e:
            print(f"Error capturing order: {e}")  # Log the error for debugging
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)





def order_confirmation_email(request):
    subject="Regarding Order Confirmation"
    from_email="omishete80@gmail.com"
    customer_details=Customer_Profile.objects.get(User=request.user)
    to_email=[customer_details.User.email]
    print(to_email)
    order_data=Order.objects.filter(user=request.user).latest("created_at")
    my_order=Order.objects.filter(user=request.user).latest("created_at")
    dishes=OrderDish.objects.filter(order=my_order)

    context={
        "user":request.user,
        "dishes":dishes,
        "total_price":order_data.total_price,
    }
    text_content=render_to_string("emails/order_confirmation.txt",context)
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.send()

    return render(request,"core/home.html")



    


    



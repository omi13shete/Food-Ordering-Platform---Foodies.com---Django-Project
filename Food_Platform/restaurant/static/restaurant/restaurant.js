let plusIcons = document.querySelectorAll(".plus-cart");

plusIcons.forEach(function(plusIcon) {
    plusIcon.addEventListener("click", function() {
        let pid = plusIcon.getAttribute("pid");
        console.log(pid);

        $.ajax({
            type: "GET",
            url: '/restaurant/cart_plus_icon_click',
            data: {
                prod_id: pid
            },
            success: function(data) {
                console.log(data);
                let parentContainer = plusIcon.closest(".cart_data_container");
                let quantityElement = parentContainer.querySelector(".quantity");
                quantityElement.innerHTML = data.quantity;
                document.getElementById("total_price").innerHTML = data.total_price;
            }
        });
    });
});



let minusIcons=document.querySelectorAll(".minus-cart")
minusIcons.forEach(function(minusIcon){
    minusIcon.addEventListener("click",function(){
        pid=minusIcon.getAttribute("pid")
        console.log("minusIcon :",pid)
       
       $.ajax({
        type:"GET",
        url:"/restaurant/cart_minus_icon_click",
        data:{
            "prod_id":pid
        },
        success:function(data){
            console.log(data)
            let parentContainer = minusIcon.closest(".cart_data_container");
            let quantityElement = parentContainer.querySelector(".quantity");
            console.log(quantityElement)
            quantityElement.innerHTML = data.dish_quantity;
            // document.getElementById("quantity").innerHTML=data.dish_quantity;
            document.getElementById("total_price").innerHTML=data.total_amount;
        }
       })
    })

})

// let removeButtons=document.querySelectorAll("remove-cart")
// removeButton.addEventListener("click",function(){
//     pid=minusIcon.getAttribute("pid")
//     console.log("removebutton :",pid)
   
//    $.ajax({
//     type:"GET",
//     url:"/restaurant/cart_remove_button_click",
//     data:{
//         "prod_id":pid
//     },
//     success:function(data){
//         console.log(data)
//         document.getElementById("total_price").innerHTML=data.total_amount;
//         document.getElementById("cart_data").style.display="None";
        

//     }
//    })
// })

let removeButtons=document.querySelectorAll(".remove-cart");
console.log(removeButtons)
removeButtons.forEach(function(removeButton){
    removeButton.addEventListener("click",function(){
    pid=removeButton.getAttribute("pid")
    console.log("removebutton :",pid)
   
   $.ajax({
    type:"GET",
    url:"/restaurant/cart_remove_button_click",
    data:{
        "prod_id":pid
    },
    success:function(data){
        console.log(data)
        parentContainer=removeButton.closest(".cart_data_container")
        parentContainer.style.display="None";
        document.getElementById("total_price").innerHTML=data.total_amount;
        

    }
   })
})

})

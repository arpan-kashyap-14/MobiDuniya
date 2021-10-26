var setProduct1 = false
var setProduct2 = false


$('#slider1, #slider2, #slider3, #slider4, #slider5, #slider6').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})
$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount



        }
    })
})


$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount


        }
    })
})


$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var eml = this
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function (data) {
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
            document.getElementById("shipping").innerHTML = `Rs. ${data.shipping_amount}`
            console.log(data.totalamount)
            if (data.totalamount == 0) {

                window.location.reload();

            }
        }
    })
});


const getProducts = () => {
    const val = $('#brand1').val()
    
    if(val == ""){
        $("#message").html("")
        $("#message").attr("class","");
        $("#message").attr("style","color:#ccc;");
        $("#product-features").html(`
        <div class="alert alert-success my-2 text-center">Please Select the products to compare</div>
        `)
        const compareBtn = document.getElementById("compare-btn");
            compareBtn.style.boxShadow = "none";
            const product1 = document.getElementById('product1')
            product1.innerHTML = '<option value="">Select The Product</option>'
            const product1Carousel = document.getElementById("product1-carousel");
    product1Carousel.innerHTML = ''

        
        return;
    }

    const product1 = document.getElementById('product1')

    product1.innerHTML = '<option value="">Select the product</option>'
    $.ajax({
        type: 'GET',
        url: '/compare/getProduct',
        contentType: 'application/json',
        data: { brandName: val },
        success: function (data) {
            
            data.responsedata.map((item) => {
                product1.innerHTML += `
                 <option value="${item[0]}">${item[1]}</option>
                 `
            })

        },
        error: function (error) {
            console.log(error)
        }

    })

}



const getProductsTwo = () => {
    const val = $('#brand2').val()

    if(val == ""){
        $("#message").html("")
        $("#message").attr("class","");
        $("#message").attr("style","color:#ccc;"); 
        $("#product-features").html(`
        <div class="alert alert-success my-2 text-center">Please Select the products to compare</div>
        `)
        const compareBtn = document.getElementById("compare-btn");
            compareBtn.style.boxShadow = "none";
            const product2 = document.getElementById('product2')
    product2.innerHTML = '<option value="">Select The Product</option>'
    const product2Carousel = document.getElementById("product2-carousel");
    product2Carousel.innerHTML = ''


        return;
    }

    const product2 = document.getElementById('product2')
    product2.innerHTML = '<option value="">Select The Product</option>'
    $.ajax({
        type: 'GET',
        url: '/compare/getProduct',
        contentType: 'application/json',
        data: { brandName: val },
        success: function (data) {

            data.responsedata.map((item) => {
                product2.innerHTML += `
                 <option value="${item[0]}">${item[1]}</option>
                 `
            })

        },
        error: function (error) {
            console.log(error)
        }

    })

}



const showProducts = () => {

    const product_id = $('#product1').val()
    const product1Carousel = document.getElementById("product1-carousel");
    product1Carousel.innerHTML = ''
    $.ajax({
        type: 'GET',
        url: "/compare/showProducts",
        contentType: "application/json",
        data: { id: product_id },
        success: function (data) {
            console.log(data.responseData)

            images = data.responseData.slice(6, 10)
            console.log(images)

            product1Carousel.innerHTML += `
           <div class="carousel-item active h-100">
               <div class="imgbx shadow" style="height:280px; background:#fefefe;">
               <img src="http://127.0.0.1:8000/media/${data.responseData[5]}" alt="" class="d-block w-100">
               </div>
            </div>
           `;

            images.map((img) => {
                product1Carousel.innerHTML += `
            <div class="carousel-item h-100">
                <div class="imgbx shadow" style="height:280px; background:#fefefe;">
                <img src="http://127.0.0.1:8000/media/${img}" alt="" class="d-block w-100">
                </div>
             </div>
            `;
            });

            const compareBtn = document.getElementById("compare-btn");
            compareBtn.style.boxShadow = "none";
            setProduct1 = true


        },
        error: function (error) {
            console.log(error)
        }
    });
}

const showProductsTwo = () => {

    const product_id = $('#product2').val()
    const product2Carousel = document.getElementById("product2-carousel");
    product2Carousel.innerHTML = ''
    $.ajax({
        type: 'GET',
        url: "/compare/showProducts",
        contentType: "application/json",
        data: { id: product_id },
        success: function (data) {
            console.log(data.responseData)

            images = data.responseData.slice(6, 10)
            console.log(images)

            product2Carousel.innerHTML += `
             <div class="carousel-item active h-100">
                 <div class="imgbx shadow" style="height:280px; background:#fefefe;">
                 <img src="http://127.0.0.1:8000/media/${data.responseData[5]}" alt="" class="d-block w-100">
                 </div>
              </div>
             `;

            images.map((img) => {
                product2Carousel.innerHTML += `
              <div class="carousel-item h-100">
                  <div class="imgbx shadow" style="height:280px; background:#fefefe;">
                  <img src="http://127.0.0.1:8000/media/${img}" alt="" class="d-block w-100">
                  </div>
               </div>
              `;
            });

            const compareBtn = document.getElementById("compare-btn");
            compareBtn.style.boxShadow = "none";
            setProduct2 = true;

        },
        error: function (error) {
            console.log(error)
        }
    });
}

const outputVoice = (txt) => {
    const msg = new SpeechSynthesisUtterance();
    msg.text = `${txt}`;
    window.speechSynthesis.speak(msg);
}

const suggestPhone = () =>{
   const brand1 = $("#brrand1").text(); 
   const brand2 = $("#brrand2").text(); 
   const modal1 = $("#modal1").text(); 
   const modal2 = $("#modal2").text(); 

   const price1 = $("#price1").text().split(' ')[1];
   const price2 = $("#price2").text().split(' ')[1];
   const battery1 = $("#battery1").text().split(" ")[0];    
   const battery2 = $("#battery2").text().split(" ")[0];    
   const ram1 = $("#ram1").text().split(" ")[0];
   const ram2 = $("#ram2").text().split(" ")[0];
   const rom1 = $("#rom1").text().split(" ")[0];
   const rom2 = $("#rom2").text().split(" ")[0];
   const front1 = $("#front1").text().split(" ")[0];
   const front2 = $("#front2").text().split(" ")[0];
   const rear1 = $("#rear1").text().split(" ")[0];
   const rear2 = $("#rear2").text().split(" ")[0];



let product1 = 0;
let product2 = 0;

//Price
if(price1<=price2){
    if(price1!=price2){
        product1+=1;
    }
}else{
    product2+=1;
}

//Battery
if(battery1>=battery2){
    if(battery1!=battery2){
        product1+=1;
    }
}else{
    product2+=1;
}

//RAM
if(ram1>=ram2){
    if(ram1!=ram2){
        product1+=1;
    }
}else{
    product2+=1;
}

//Internal Storage
if(rom1>=rom2){
    if(rom1!=rom2){
        product1+=1;
    }
}else{
    product2+=1;
}

//Rear Camera
if(rear1>=rear2){
    if(rear1!=rear2){
        product1+=1;
    }
}else{
    product2+=1;
}

//Front Camera
if(front1>=front2){
    if(front1!=front2){
        product1+=1;
    }
}else{
    product2+=1;
}

let msg1 = `According to Brainy, you should go for ${brand1}  ${modal1}`
let msg2 = `According to Brainy, you should go for ${brand2}  ${modal2}`

if(product1 == product2){
    if(price1<price2){
        //Output Voice with message = "According to Brainy, you should go for " + brand1 + " " + model1
        $("#message").html(msg1)
        $("#message").attr("class","dark-header-1 mt-3 p-2");
        $("#message").attr("style","color:#ccc;");
        outputVoice(msg1)
    } else {
        if(price2<price1){
            //Output Voice with message = "According to Brainy, you should go for " + brand2 + " " + model2
        $("#message").html(msg2)
        $("#message").attr("class","dark-header-1 mt-3 p-2");
        $("#message").attr("style","color:#ccc;");
        outputVoice(msg2)

           
        }
        else {
            //Output Voice with message = "According to Brainy, both the products proves equal when compared "
        $("#message").html(`According to Brainy, both the products proves equal when compared `)
        $("#message").attr("class","dark-header-1 mt-3 p-2");
        $("#message").attr("style","color:#ccc;");
        outputVoice(`According to Brainy, both the products proves equal when compared `)
        }
    }
} else {
    if(product1>product2){
        //Output Voice with message = "According to Brainy, you should go for " + brand1 + " " + model1
        $("#message").html(msg1)
        $("#message").attr("class","dark-header-1 mt-3 p-2");
        $("#message").attr("style","color:#ccc;");
        outputVoice(msg1)

    } else {
        //Output Voice with message = "According to Brainy, you should go for " + brand2 + " " + model2
        $("#message").html(msg2)
        $("#message").attr("class","dark-header-1 mt-3 p-2");
        $("#message").attr("style","color:#ccc;");
        outputVoice(msg2)

    }
}

   

}

const showFeatures = () => {
    const compareBtn = document.getElementById("compare-btn");
    compareBtn.style.boxShadow = "4px 4px 20px #fff";
    const renderProduct = document.getElementById("product-features");
    const productId1 = $("#product1").val()
    const productId2 = $("#product2").val()

    renderProduct.innerHTML = " ";


    if (setProduct1 || setProduct2) {

        console.log(productId1)
        console.log(productId2)

        $.ajax({
            type: "GET",
            url: "/compare/getFeatures",
            contentType: "application/json",
            data: {
                product_id_1: productId1,
                product_id_2: productId2
            },
            success: function (data) {
                console.log(data.productData)
                if (data) {
                    const general = data.productData.slice(0, 7)
                    const display = data.productData.slice(7, 11)
                    const hardware = data.productData.slice(11, 14)
                    const camera = data.productData.slice(14, 16)
                    

                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
        <div class="col-sm-12">
            <table class="table table-bordered table-light shadow">
                <tHead >
                    <tr class="table-dark">
                        <th colspan="3">General</th>
                        
                    </tr>
                    <tr>
                        <th>Features</th>
                        <th>${general[0][0]} ${general[1][0]}</th>
                        <th>${general[0][1]} ${general[1][1]}</th>
                    </tr>
                </tHead>

                <tBody class="text-black">
                    <tr>
                        <td>Brand</td>
                        <td id="brrand1" >${general[0][0]}</td>
                        <td id="brrand2">${general[0][1]}</td>
                        
                    </tr>
                    <tr>
                        <td>Model</td>
                        <td id="modal1">${general[1][0]}</td>
                        <td id="modal2">${general[1][1]}</td>
                    
                    </tr>
                    <tr>
                        <td>Price</td>
                        <td id="price1"   >Rs. ${general[2][0]}</td>
                        <td id="price2" >Rs. ${general[2][1]}</td>
                        

                    </tr>
                    <tr>
                        <td>Launch in India</td>
                        <td>Yes</td>
                        <td>Yes</td>

                    </tr>
                    <tr>
                        <td>Form Factor</td>
                        <td>Touch Screen</td>
                        <td>Touch Screen</td>

                    </tr>
                    <tr>
                        <td>Body Length</td>
                        <td>${general[3][0]}</td>
                        <td>${general[3][1]}</td>
                        

                    </tr>
                    <tr>
                        <td>Body Width</td>
                        <td>${general[4][0]}</td>
                        <td>${general[4][1]}</td>
                

                    </tr>
                    <tr>
                        <td>Body Weight</td>
                        <td>${general[5][0]}</td>
                        <td>${general[5][1]}</td>
                    </tr>
                    <tr>
                        <td>Battery</td>
                        <td id="battery1" >${general[6][0]}</td>
                        <td id="battery2" >${general[6][1]}</td>
                    </tr>

                </tBody>

            </table>
        </div>
                        </div>`

                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
                        <div class="col-sm-12">
                            
                            <table class="table table-bordered table-light shadow">
                                <tHead >
                                    <tr class="table-dark">
                                        <th colspan="3">Display</th>
                                        
                                    </tr>
                                    <tr>
                                    <th>Features</th>
                                    <th>${general[0][0]} ${general[1][0]}</th>
                                    <th>${general[0][1]} ${general[1][1]}</th>
                                    </tr>
                                </tHead>
                                <tBody class="text-black">

                                    <tr>
                                        <td>Display</td>
                                        <td>${display[0][0]}</td>
                                        <td>${display[0][1]}</td>
                                    </tr>

                                    <tr>
                                        <td>TouchScreen</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>

                                    <tr>
                                        <td>Resolution</td>
                                        <td>${display[1][0]} px</td>
                                        <td>${display[1][1]}</td>
                                    </tr>

                                    <tr>
                                        <td>Aspect Ratio</td>
                                        <td>${display[2][0]}</td>
                                        <td>${display[2][1]}</td>
                                    </tr>

                                    <tr>
                                        <td>Refresh Rate</td>
                                        <td>${display[3][0]}</td>
                                        <td>${display[3][1]}</td>
                                    </tr>
                                </tBody>
                            </table>
                        </div>
                        </div>`

                        renderProduct.innerHTML +=`
                        <div class="row mt-sm-3 mt-lg-4">
                                <div class="col-sm-12">
                                    
                                    <table class="table table-bordered table-light shadow">
                                        <tHead >
                                            <tr class="table-dark">
                                                <th colspan="3">Hardware</th>
                                                
                                            </tr>
                                            <tr>
                                            <th>Features</th>
                                            <th>${general[0][0]} ${general[1][0]}</th>
                                            <th>${general[0][1]} ${general[1][1]}</th>
                                            </tr>
                                        </tHead>
                                        <tBody class="text-black">

                                            <tr>
                                                <td>Processor</td>
                                                <td>${hardware[0][0]}</td>
                                                <td>${hardware[0][1]}</td>
                                            </tr>

                                            <tr>
                                                <td>RAM</td>
                                                <td id="ram1" >${hardware[1][0]} GB</td>
                                                <td id="ram2" >${hardware[1][1]} GB</td>
                                            </tr>

                                            <tr>
                                                <td>Internal Storage</td>
                                                <td id="rom1" >${hardware[2][0]} GB</td>
                                                <td id="rom2">${hardware[2][1]} GB</td>
                                            </tr>

                                            <tr>
                                                <td>Expandable Storage</td>
                                                <td>Yes</td>
                                                <td>Yes</td>
                                            </tr>

                                            <tr>
                                                <td>Expandable Storage type</td>
                                                <td>microSD</td>
                                                <td>microSD</td>
                                            </tr>
                                        </tBody>
                                    </table>
                                </div>
                            </div>
                        `
                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
        <div class="col-sm-12">
            
            <table class="table table-bordered table-light shadow">
                <tHead >
                    <tr class="table-dark">
                        <th colspan="3">Camera</th>
                        
                    </tr>
                    <tr>
                    <th>Features</th>
                        <th>${general[0][0]} ${general[1][0]}</th>
                        <th>${general[0][1]} ${general[1][1]}</th>
                    </tr>
                </tHead>
                <tBody class="text-black">

                    <tr>
                        <td>Rear Camera</td>
                        <td id="rear1" >${camera[0][0]}</td>
                        <td id="rear2">${camera[0][1]}</td>
                    </tr>

                    <tr>
                        <td>Rear Flash</td>
                        <td>dual LED</td>
                        <td>dual LED</td>
                    </tr>

                    <tr>
                        <td>Front Camera</td>
                        <td id="front1" >${camera[1][0]}</td>
                        <td id="front2" >${camera[1][1]}</td>
                    </tr>

                </tBody>
            </table>
        </div>
    </div>
                        `
                         
                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
        <div class="col-sm-12">
            
            <table class="table table-bordered table-light shadow">
                <tHead >
                    <tr class="table-dark">
                        <th colspan="3">Software</th>
                        
                    </tr>
                    <tr>
                    <th>Features</th>
                        <th>${general[0][0]} ${general[1][0]}</th>
                        <th>${general[0][1]} ${general[1][1]}</th>
                    </tr>
                </tHead>
                <tBody class="text-black">

                    <tr>
                        <td>Operating System</td>
                        <td>${data.productData[16][0]}</td>
                        <td>${data.productData[16][1]}</td>
                    </tr>
                </tBody>
            </table>
        </div>
    </div>
                        `
                                
                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
                        <div class="col-sm-12">
                            <table class="table table-bordered table-light shadow">
                                <tHead >
                                    <tr class="table-dark">
                                        <th colspan="3">Connectivity</th>
                                        
                                    </tr>
                                    <tr>
                                    <th>Features</th>
                        <th>${general[0][0]} ${general[1][0]}</th>
                        <th>${general[0][1]} ${general[1][1]}</th>
                                    </tr>
                                </tHead>
                                <tBody class="text-black">
                                    <tr>
                                        <td>Wi-Fi</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>GPS</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Bluetooth</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>USB OTG</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Headphones</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Microphone</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>FM</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Number of SIMs</td>
                                        <td>2</td>
                                        <td>2</td>
                                    </tr>
                
                                </tBody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="row mt-sm-3 mt-lg-4">
                        <div class="col-sm-12">
                            
                            <table class="table table-bordered table-light shadow ">
                                <tHead >
                                    <tr class="table-dark">
                                        <th colspan="3">Sensors</th>
                                        
                                    </tr>
                                    <tr>
                                    <th>Features</th>
                                    <th>${general[0][0]} ${general[1][0]}</th>
                                    <th>${general[0][1]} ${general[1][1]}</th>
                                    </tr>
                                </tHead>
                                <tBody class="text-black">
                
                                    <tr>
                                        <td>Face Unlock</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>FingerPrint</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Compass/Magnetometer</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Promixity Sensor</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Accelerometer</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Ambient Light Sensor</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Gyroscope</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                                </tBody>
                            </table>
                        </div>
                    </div>
                        `

                 suggestPhone();  
                }
            },
            error: function (error) {
                console.log(error)
            }
        })



    } else {
        alert("please select product")
    }





}


// second compare page 

const showFeaturesView = () => {
    const compareBtn = document.getElementById("compare-btn");
    compareBtn.style.boxShadow = "4px 4px 20px #fff";
    const renderProduct = document.getElementById("product-features");
    const productId1 = $("#product1").val()
    const productId2 = $("#product2").val()

    renderProduct.innerHTML = " ";
    if (setProduct2) {
       
         console.log('product1',productId1)
         console.log(productId2)

        $.ajax({
            type: "GET",
            url: "/compare/getFeatures",
            contentType: "application/json",
            data: {
                product_id_1: productId1,
                product_id_2: productId2
            },
            success: function (data) {
                console.log(data.productData)
                if (data) {
                    const general = data.productData.slice(0, 7)
                    const display = data.productData.slice(7, 11)
                    const hardware = data.productData.slice(11, 14)
                    const camera = data.productData.slice(14, 16)
                    

                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
        <div class="col-sm-12">
            <table class="table table-bordered table-light shadow">
                <tHead >
                    <tr class="table-dark">
                        <th colspan="3">General</th>
                        
                    </tr>
                    <tr>
                        <th>Features</th>
                        <th>${general[0][0]} ${general[1][0]}</th>
                        <th>${general[0][1]} ${general[1][1]}</th>
                    </tr>
                </tHead>

                <tBody class="text-black">
                    <tr>
                        <td>Brand</td>
                        <td id="brrand1" >${general[0][0]}</td>
                        <td id="brrand2">${general[0][1]}</td>
                        
                    </tr>
                    <tr>
                        <td>Model</td>
                        <td id="modal1">${general[1][0]}</td>
                        <td id="modal2">${general[1][1]}</td>
                    
                    </tr>
                    <tr>
                        <td>Price</td>
                        <td id="price1"   >Rs. ${general[2][0]}</td>
                        <td id="price2" >Rs. ${general[2][1]}</td>
                        

                    </tr>
                    <tr>
                        <td>Launch in India</td>
                        <td>Yes</td>
                        <td>Yes</td>

                    </tr>
                    <tr>
                        <td>Form Factor</td>
                        <td>Touch Screen</td>
                        <td>Touch Screen</td>

                    </tr>
                    <tr>
                        <td>Body Length</td>
                        <td>${general[3][0]}</td>
                        <td>${general[3][1]}</td>
                        

                    </tr>
                    <tr>
                        <td>Body Width</td>
                        <td>${general[4][0]}</td>
                        <td>${general[4][1]}</td>
                

                    </tr>
                    <tr>
                        <td>Body Weight</td>
                        <td>${general[5][0]}</td>
                        <td>${general[5][1]}</td>
                    </tr>
                    <tr>
                        <td>Battery</td>
                        <td id="battery1" >${general[6][0]}</td>
                        <td id="battery2" >${general[6][1]}</td>
                    </tr>

                </tBody>

            </table>
        </div>
                        </div>`

                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
                        <div class="col-sm-12">
                            
                            <table class="table table-bordered table-light shadow">
                                <tHead >
                                    <tr class="table-dark">
                                        <th colspan="3">Display</th>
                                        
                                    </tr>
                                    <tr>
                                    <th>Features</th>
                                    <th>${general[0][0]} ${general[1][0]}</th>
                                    <th>${general[0][1]} ${general[1][1]}</th>
                                    </tr>
                                </tHead>
                                <tBody class="text-black">

                                    <tr>
                                        <td>Display</td>
                                        <td>${display[0][0]}</td>
                                        <td>${display[0][1]}</td>
                                    </tr>

                                    <tr>
                                        <td>TouchScreen</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>

                                    <tr>
                                        <td>Resolution</td>
                                        <td>${display[1][0]} px</td>
                                        <td>${display[1][1]}</td>
                                    </tr>

                                    <tr>
                                        <td>Aspect Ratio</td>
                                        <td>${display[2][0]}</td>
                                        <td>${display[2][1]}</td>
                                    </tr>

                                    <tr>
                                        <td>Refresh Rate</td>
                                        <td>${display[3][0]}</td>
                                        <td>${display[3][1]}</td>
                                    </tr>
                                </tBody>
                            </table>
                        </div>
                        </div>`

                        renderProduct.innerHTML +=`
                        <div class="row mt-sm-3 mt-lg-4">
                                <div class="col-sm-12">
                                    
                                    <table class="table table-bordered table-light shadow">
                                        <tHead >
                                            <tr class="table-dark">
                                                <th colspan="3">Hardware</th>
                                                
                                            </tr>
                                            <tr>
                                            <th>Features</th>
                                            <th>${general[0][0]} ${general[1][0]}</th>
                                            <th>${general[0][1]} ${general[1][1]}</th>
                                            </tr>
                                        </tHead>
                                        <tBody class="text-black">

                                            <tr>
                                                <td>Processor</td>
                                                <td>${hardware[0][0]}</td>
                                                <td>${hardware[0][1]}</td>
                                            </tr>

                                            <tr>
                                                <td>RAM</td>
                                                <td id="ram1" >${hardware[1][0]} GB</td>
                                                <td id="ram2" >${hardware[1][1]} GB</td>
                                            </tr>

                                            <tr>
                                                <td>Internal Storage</td>
                                                <td id="rom1" >${hardware[2][0]} GB</td>
                                                <td id="rom2">${hardware[2][1]} GB</td>
                                            </tr>

                                            <tr>
                                                <td>Expandable Storage</td>
                                                <td>Yes</td>
                                                <td>Yes</td>
                                            </tr>

                                            <tr>
                                                <td>Expandable Storage type</td>
                                                <td>microSD</td>
                                                <td>microSD</td>
                                            </tr>
                                        </tBody>
                                    </table>
                                </div>
                            </div>
                        `
                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
        <div class="col-sm-12">
            
            <table class="table table-bordered table-light shadow">
                <tHead >
                    <tr class="table-dark">
                        <th colspan="3">Camera</th>
                        
                    </tr>
                    <tr>
                    <th>Features</th>
                        <th>${general[0][0]} ${general[1][0]}</th>
                        <th>${general[0][1]} ${general[1][1]}</th>
                    </tr>
                </tHead>
                <tBody class="text-black">

                    <tr>
                        <td>Rear Camera</td>
                        <td id="rear1" >${camera[0][0]}</td>
                        <td id="rear2">${camera[0][1]}</td>
                    </tr>

                    <tr>
                        <td>Rear Flash</td>
                        <td>dual LED</td>
                        <td>dual LED</td>
                    </tr>

                    <tr>
                        <td>Front Camera</td>
                        <td id="front1" >${camera[1][0]}</td>
                        <td id="front2" >${camera[1][1]}</td>
                    </tr>

                </tBody>
            </table>
        </div>
    </div>
                        `
                         
                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
        <div class="col-sm-12">
            
            <table class="table table-bordered table-light shadow">
                <tHead >
                    <tr class="table-dark">
                        <th colspan="3">Software</th>
                        
                    </tr>
                    <tr>
                    <th>Features</th>
                        <th>${general[0][0]} ${general[1][0]}</th>
                        <th>${general[0][1]} ${general[1][1]}</th>
                    </tr>
                </tHead>
                <tBody class="text-black">

                    <tr>
                        <td>Operating System</td>
                        <td>${data.productData[16][0]}</td>
                        <td>${data.productData[16][1]}</td>
                    </tr>
                </tBody>
            </table>
        </div>
    </div>
                        `
                                
                        renderProduct.innerHTML += `
                        <div class="row mt-sm-3 mt-lg-4">
                        <div class="col-sm-12">
                            <table class="table table-bordered table-light shadow">
                                <tHead >
                                    <tr class="table-dark">
                                        <th colspan="3">Connectivity</th>
                                        
                                    </tr>
                                    <tr>
                                    <th>Features</th>
                        <th>${general[0][0]} ${general[1][0]}</th>
                        <th>${general[0][1]} ${general[1][1]}</th>
                                    </tr>
                                </tHead>
                                <tBody class="text-black">
                                    <tr>
                                        <td>Wi-Fi</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>GPS</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Bluetooth</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>USB OTG</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Headphones</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Microphone</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>FM</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Number of SIMs</td>
                                        <td>2</td>
                                        <td>2</td>
                                    </tr>
                
                                </tBody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="row mt-sm-3 mt-lg-4">
                        <div class="col-sm-12">
                            
                            <table class="table table-bordered table-light shadow ">
                                <tHead >
                                    <tr class="table-dark">
                                        <th colspan="3">Sensors</th>
                                        
                                    </tr>
                                    <tr>
                                    <th>Features</th>
                                    <th>${general[0][0]} ${general[1][0]}</th>
                                    <th>${general[0][1]} ${general[1][1]}</th>
                                    </tr>
                                </tHead>
                                <tBody class="text-black">
                
                                    <tr>
                                        <td>Face Unlock</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>FingerPrint</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Compass/Magnetometer</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Promixity Sensor</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Accelerometer</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Ambient Light Sensor</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                
                                    <tr>
                                        <td>Gyroscope</td>
                                        <td>Yes</td>
                                        <td>Yes</td>
                                    </tr>
                                </tBody>
                            </table>
                        </div>
                    </div>
                        `

                 suggestPhone();  
                }
            },
            error: function (error) {
                console.log(error)
            }
        })



    } else {
        alert("please select product")
    }





}

// second compare page 


// suggest page ajax
const suggestPhones = (e) =>{
    //  e.preventDefault;

    const brand = {
        vivo: $('#check-vivo').is(":checked") ? true : false,
        oppo: $('#check-oppo').is(":checked") ? true : false,
        samsung: $('#check-samsung').is(":checked") ? true : false,
        realme: $('#check-realme').is(":checked") ? true : false,
        xiaomi: $('#check-xiaomi').is(":checked") ? true : false,
        oneplus: $('#check-oneplus').is(":checked") ? true : false,
    }

    const productObj ={
     ...brand,   
     price : $("#sprice").val(),
     ram : $("#sram").val(),
     internal : $("#sinternal").val(),
     display : $("#sdisplay").val(),
     processor : $("#sprocessor").val(),
     front_camera : $("#sfrontCamera").val().split(' ')[0],
     rear_camera : $("#srearCamera").val().split(' ')[0],

    };

    if( !(brand.vivo || brand.oppo || brand.realme || brand.oneplus || brand.xiaomi || brand.samsung) ){
          alert("Please select at least 1 brand for suggestion");
          return;

    }else if( !productObj.price ){
         alert("Please select the price range"); 
    }
    else{
        
       $.ajax({
           type:"GET",
           url:"/suggest/suggestPhone",
           contentType:"application/json",
           data: productObj,
           success: function(data){
               if(data){

                if(data.responseData[0] == '' ){
                      outputVoice(`${data.responseData[1]}`)     
                      $("#sgstmessage").html(`<h3> ${data.responseData[1]}</h3>` )
                      $("#sgstmessage").attr("class","dark-header-1 mt-3 p-2 text-center");
                      $("#sgstmessage").attr("style","color:#ccc;");

                }else{


               const resultMsg = `${data.responseData[1]}`
               const p_id = `${data.responseData[0]}`
                $("#sgstmessage").html(`<a href="product-detail/${p_id}" >${data.responseData[1]}</a>`)
                $("#sgstmessage").attr("class","dark-header-1 mt-3 p-2 text-center");
                $("#sgstmessage").attr("style","color:#ccc;");
                $("#sgstmessage a").attr("style","color:#ccc;");
                outputVoice(resultMsg) 
            }

        }
    
    },

       })

    }

    console.log(productObj)
   
 }


// suggest page ajax

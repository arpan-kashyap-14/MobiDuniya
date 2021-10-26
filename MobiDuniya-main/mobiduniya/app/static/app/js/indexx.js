const ruppee = $('#totalamount').text();
const dollar = (parseFloat(ruppee)*0.013).toFixed(2);
$("#dollar").text(`${dollar}`)

const r =  $("#convertDollar").text().split(' ')[3];
const d = (parseFloat(r)*0.013).toFixed(2);


$("#convertDollar").html(`<p class="fw-bold dark-header-1" id="convertDollar" style="color: #ccc; padding: 5px 10px; font-size: 1.2em;">Amount Paid: &#8377 ${r} (in Dollar ${d}) </p>`);




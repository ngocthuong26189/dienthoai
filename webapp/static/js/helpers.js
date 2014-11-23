var post = function(url, data, index_url) {
  if (!data) data = {};

  // Show the dialog to confirm

  if (!confirm("Are you sure?")) return;

  $.ajax({
    url: url,
    data: data,
    type: 'POST'
  }).done(function(data) {
    alert('Done');
    if(index_url)
      window.location.href = index_url;
    else
      window.location.reload();
  }).error(function(err) {
    alert('Dafuq, something is wrong');
  });
}

function change_selling_price() {
  var price = $("input[name='price']" ).val();
  var selling_price = $("input[name='selling_price']").val();
  
  if(parseFloat(price) >= 0){
    if(parseFloat(selling_price) > parseFloat(price)){
      alert("selling price not > than price");
      $("input[name='selling_price']").val(price);
      selling_price = $("input[name='selling_price']").val();
    }
    // Math.round(n * 1000)/1000;
    var discount = ((parseFloat(price) - parseFloat(selling_price))/parseFloat(price))*100.000;
    discount = Math.round(discount * 1000)/1000;
    $("input[name='discount']" ).val(discount);
  }
  else {
    alert("input price!");
    $("input[name='selling_price']").val(0);
    selling_price = parseFloat($("input[name='selling_price']").val());
  }
}
function change_discount() {
  var price = parseFloat($("input[name='price']" ).val());
  var discount = parseFloat($("input[name='discount']" ).val());
  if(discount > 100 || discount < 0){
    alert("discount between 0 and 100");
    $("input[name='discount']" ).val(0)
    discount = parseFloat($("input[name='discount']" ).val());
  }
  if(price >= 0){
    var selling_price = price - discount * price/100;
    selling_price = Math.round(selling_price * 1000) / 1000;
    $("input[name='selling_price']" ).val(selling_price);
  }
  else {
    alert("input price!");
    $("input[name='discount']").val(0);
    discount = parseFloat($("input[name='discount']").val());
  }
}
function change_price() {
  $("input[name='selling_price']").val(null);
  $("input[name='discount']").val(null);
}
$("input[name='selling_price']" ).keyup(function () {
  change_selling_price();
});
$("input[name='discount']" ).keyup(function () {
  change_discount();
});
$("input[name='price']" ).keyup(function () {
  change_price();
});

$("input[name='price']" ).change(function () {
  change_price();
});
$("input[name='discount']" ).change(function () {
  change_discount();
});
$("input[name='selling_price']" ).change(function () {
  change_selling_price();
});
$('#panel3').on('toggled', function (event, accordion) {
    
});
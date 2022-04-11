$('.open-button').click(function(){
  $('.search').addClass('active');
  $('.overlay').removeClass('hidden');
  $('input').focus(); // If there are multiple inputs on the page you might want to use an ID
});

$('.overlay').click(function() {
  $('.search').removeClass('active');
  $(this).addClass('hidden');
});
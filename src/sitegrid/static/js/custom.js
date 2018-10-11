$(document).on('documentFadedIn',function() {

  $('#sidebar').height($('#wrapper').height());

  $(window).resize(function(){
    $('#sidebar').height($('#wrapper').height());
  });

  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  $('.sidebar-nav li a')
    .mouseover(function() {
      if( $(this)[0].className != 'active' ) {
        $(this).find('.arrow-right').show();
      }
    })
    .mouseout(function() {
      if( $(this)[0].className != 'active' ) {
        $(this).find('.arrow-right').hide();
      }
    });

  $(function(){
    $(".sidebar-nav li a").each(function(){
      if ($(this).attr("href") == window.location.pathname){
        $(this).addClass("active");
      }
      else if('/alist/create-event/' == window.location.pathname) {
        $('#create-highlight').addClass("active");
      }
    });
  });

  $("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
  });

  document.querySelector( "#nav-toggle" )
  .addEventListener( "click", function() {
    this.classList.toggle( "active" );
  });

});

function expandNav() {

  $('#sidebar').addClass('sidebar-expand');
  $('.sidebar-nav').addClass('sidebar-nav-expand');
  $('img.icon').addClass('icon-expand');
  $('.arrow-right').addClass('arrow-right-expand');
  $('.sidebar-nav li').addClass('expand');

  window.setTimeout(function(){$(".pg-name").addClass("pg-name-expand");}, 300);

  $('#expand-arrow').hide();
  $('#collapse-arrow').show();
}

function collaspeNav() {

  $('#sidebar').removeClass('sidebar-expand', 1000);
  $('.sidebar-nav').removeClass('sidebar-nav-expand', 1000);
  $('img.icon').removeClass('icon-expand', 1000);
  $('.pg-name').removeClass('pg-name-expand');
  $('.arrow-right').removeClass('arrow-right-expand', 1000);
  $('.sidebar-nav li').removeClass('expand', 1000);

  window.setTimeout(function(){$('#sidebar').removeClass('sidebar-expand-ab');}, 1000);

  $('#collapse-arrow').hide();
  $('#expand-arrow').show();
}
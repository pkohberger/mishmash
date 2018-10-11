evenOddStyle();

$('[data-toggle="tooltip"]').tooltip();

checkListType('people');

$('.title-event-admin .admins').each(function(index) {
  var admin_list = $( this ).text();
  admin_list = admin_list.replace(/,\s*$/, "");
  $('.title-event-admin .admins').text(admin_list);
});

$("button.admin-btn").click(function(){
  $("button.invite-btn").show();
  $(".exit-create-sm").show();
});

$('.exit-create-sm').click(function() {
  $("button.admin-btn").trigger('click');
  $("button.invite-btn").hide();
  $('.exit-create-sm').hide();
});

function sortNameAlist(sort_by, list_id) {
  var down = false;
  var sort_type = 'asc'

  if( $('.down-sort-name-'+list_id).is(':visible') ) {
    down = true;
    var sort_type = 'desc'
  }

  var arrow_name = 'name-'
  completeSort(sort_by, sort_type, list_id, down, arrow_name);
}

function sortGroupAlist(sort_by, list_id) {
  var down = false;
  var sort_type = 'asc'

  if( $('.down-sort-group-'+list_id).is(':visible') ) {
    down = true;
    var sort_type = 'desc'
  }

  var arrow_name = 'group-'
  completeSort(sort_by, sort_type, list_id, down, arrow_name);
}

function toggleArrows(ele) {
  if($(ele).attr('aria-expanded') == 'true') {
    $('#' + ele.id + ' .alist-up-arrow').hide();
    $('#' + ele.id + ' .alist-dw-arrow').show();
  }
  else {
    $('#' + ele.id + ' .alist-up-arrow').show();
    $('#' + ele.id + ' .alist-dw-arrow').hide();
  }
}

function showChkBoxes() {
  if($('#del-btn').text() == 'Cancel') {
    $('.del-chks').hide();
    $('#del-btn').text('Delete');
    $('.save-del').hide();
    $('.del-chks input').prop('checked', false);
    $('.list-arrows').show();
    $('.edit-icon').show();
  }
  else {
    $('.list-arrows').hide();
    $('.del-chks').show();
    $('#del-btn').text('Cancel');
    $('.save-del').show();
    $('.people-alist-row').show();
    $('.edit-icon').hide();
    $('.alist-edit-forms').hide();
  }
}

// CREATE LIST FUNCTIONS START
function checkListType(type) {
  if(type == 'people') {
    $('#materials-btn').css('background-color', '#E0E3E5');
    $('#materials-btn').css('color', '#667076');
    $('#people-btn').css('background-color', '#667076');
    $('#people-btn').css('color', '#FFF');

    $('#people-radio').trigger('click');
  }
  else if(type == 'materials') {
    $('#people-btn').css('background-color', '#E0E3E5');
    $('#people-btn').css('color', '#667076');
    $('#materials-btn').css('background-color', '#667076');
    $('#materials-btn').css('color', '#FFF');

    $('#materials-radio').trigger('click');
  }
}
// CREATE LIST FUNCTIONS ENDED

// ADD PEOPLE FUNCTIONS START
function addMoreD(id) {
    var deliverable_html = $('#deliverable-html-' + id).html();
    var deliverable_qty_html = $('#deliverable-qty-html-' + id).html();
    $("#deliverable-html").before( deliverable_html );
    $("#deliverable-qty-html").before( deliverable_qty_html );

    $("#deliverable-html-mobile").before( deliverable_html );
    $("#deliverable-qty-html-mobile").before( deliverable_qty_html );
}

function addMoreDEdit(list_id, alist_id) {
    var deliverable_html = $('#deliverable-html-' + list_id).html();
    var deliverable_qty_html = $('#deliverable-qty-html-' + list_id).html();
    $("#extra-deliverable-edit-" + alist_id).before( deliverable_html );
    $("#extra-deliverable-qty-edit-" + alist_id).before( deliverable_qty_html );

    $("#extra-deliverable-edit-mobile-" + alist_id).before( deliverable_html );
    $("#extra-deliverable-qty-edit-mobile-" + alist_id).before( deliverable_qty_html );
}

function addMoreR(id) {
    var returnable_html = $('#returnable-html-' + id).html();
    $("#returnable-html").before( returnable_html );
    $("#returnable-html-mobile").before( returnable_html );
}

function addMoreREdit(list_id, alist_id) {
    var returnable_html = $('#returnable-html-' + list_id).html();
    
    $("#extra-returnable-edit-mobile-" + alist_id).before( returnable_html );
}
// ADD PEOPLE FUNCTIONS ENDED

// ADD PLUS ONE FUNCTIONS START
function addPlusOne(list_id, alist_id) {

  var ele = $('.people-alist-desktop ' + '#plus-alist-form-' + alist_id)[0].previousElementSibling;

  if( $(ele).hasClass('even') ) {
    $('.people-alist-desktop ' + '#plus-alist-form-' + alist_id).addClass('odd');
  }
  else {
    $('.people-alist-desktop ' + '#plus-alist-form-' + alist_id).addClass('even');
  }

  $('.people-alist-desktop ' + '#plus-alist-form-' + alist_id).show();
  $('.people-alist-desktop ' + '#plus-btn-' + alist_id).hide();
  $('.people-alist-desktop ' + '#minus-btn-' + alist_id).show();

  $('.people-alist-desktop ' + '#people-add-btn-' + list_id).hide();
  $('.people-alist-desktop ' + '#people-save-btn-' + list_id).hide();
  $('.people-alist-desktop ' + '#people-alist-form-' + list_id).hide();

  var ele = $('.people-alist-mobile ' + '#plus-alist-form-' + alist_id)[0].previousElementSibling;

  if( $(ele).hasClass('even') ) {
    $('.people-alist-mobile ' + '#plus-alist-form-' + alist_id).addClass('odd');
  }
  else {
    $('.people-alist-mobile ' + '#plus-alist-form-' + alist_id).addClass('even');
  }

  $('.people-alist-mobile ' + '#plus-alist-form-' + alist_id).show();
  $('.people-alist-mobile ' + '#plus-btn-' + alist_id).hide();
  $('.people-alist-mobile ' + '#minus-btn-' + alist_id).show();

  $('.people-alist-mobile ' + '#people-add-btn-' + list_id).hide();
  $('.people-alist-mobile ' + '#people-save-btn-' + list_id).hide();
  $('.people-alist-mobile ' + '#people-alist-form-' + list_id).hide();
}
function minusPlusOne(list_id, alist_id) {
  $('.people-alist-desktop ' + '#plus-alist-form-' + alist_id).hide();
  $('.people-alist-desktop ' + '#minus-btn-' + alist_id).hide();
  $('.people-alist-desktop ' + '#plus-btn-' + alist_id).show();

  $('.people-alist-desktop ' + '#people-add-btn-' + list_id).show();

  $('.people-alist-mobile ' + '#plus-alist-form-' + alist_id).hide();
  $('.people-alist-mobile ' + '#minus-btn-' + alist_id).hide();
  $('.people-alist-mobile ' + '#plus-btn-' + alist_id).show();

  $('.people-alist-mobile ' + '#people-add-btn-' + list_id).show();
}
// ADD PLUS ONE FUNCTIONS END

function showHideArrows(ele) {
  if ($('#' + ele.id + ' #up.list-drop-arrow').is(':visible')) {
    $('#' + ele.id + ' #up.list-drop-arrow').hide();
    $('#' + ele.id + ' #down.list-drop-arrow').show();
  }
  else {
    $('#' + ele.id + ' #down.list-drop-arrow').hide();
    $('#' + ele.id + ' #up.list-drop-arrow').show();
  }
}

function addAdminToEventCreate() {
  $('.selected-listadmin-list').text('');
  var list = '';

  $('#admins input:checkbox').each(function(i, obj) {
    if(obj.checked) {
      name = $('#admins .user-' + obj.id).text();
      list = list + name + ', ';
    }
  });

  $('.selected-listadmin-list').text(list);
  if (list == '') {
    $('.selected-listadmin-list').text('List Admin, Name Here');
  }
}

function addAdminToEvent(id) {
  if(id != undefined) {
    $('.selected-listadmin-list-' + id).text('');
    var list = '';

    $('#admins-' + id + ' input:checkbox').each(function(i, obj) {
      if(obj.checked) {
        name = $('#admins-' + id + ' .user-' + obj.id).text();
        list = list + name + ', ';
      }
    });

    $('.selected-listadmin-list-' + id).text(list);
    if (list == '') {
      $('.selected-listadmin-list-' + id).text('List Admin, Name Here');
    }
  }
  else {
    addAdminToEventCreate();
  }
}

function evenOddStyle() {
  $ ('.people-alist-desktop .people-alist-row:even').addClass('even');
  $ ('.people-alist-desktop .people-alist-row:odd').addClass('odd');
  $ ('.people-alist-mobile .people-alist-row:even').addClass('even');
  $ ('.people-alist-mobile .people-alist-row:odd').addClass('odd');
  $('.people-alist-mobile .more-alist:even').addClass('even');
  $('.people-alist-mobile .more-alist:odd').addClass('odd');

  $ ('.materials-alist-desktop .material-alist-row:even').addClass('even');
  $ ('.materials-alist-desktop .material-alist-row:odd').addClass('odd');
  $ ('.materials-alist-mobile .material-alist-row:even').addClass('even');
  $ ('.materials-alist-mobile .material-alist-row:odd').addClass('odd');
  $('.materials-alist-mobile .more-alist:even').addClass('even');
  $('.materials-alist-mobile .more-alist:odd').addClass('odd');

  $('.alist-edit-forms:even').addClass('even');
  $('.alist-edit-forms:odd').addClass('odd');
}

function showForm(type, id) {
  $('.people-alist-desktop ' + '#' + type + '-alist-form-' + id).show();
  $('.materials-alist-desktop ' + '#' + type + '-alist-form-' + id).show();

  $('.people-alist-mobile ' + '#' + type + '-alist-form-' + id).show();
  $('.materials-alist-mobile ' + '#' + type + '-alist-form-' + id).show();

  $('#' + type + '-add-btn-' + id).hide();
  $('#' + type + '-save-btn-' + id).show();
}

function editView(id) {
  $('.edit-icon').hide();

  $('#'+id).hide();
  $('#mobile-'+id).hide();

  $('.people-alist-desktop #people-alist-edit-form-'+id).show();
  $('.people-alist-mobile #people-alist-edit-form-'+id).show();

  $('.materials-alist-desktop #materials-alist-edit-form-'+id).show();
  $('.materials-alist-mobile #materials-alist-edit-form-'+id).show();
}

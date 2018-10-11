function editViewAccountInfo(section, form) {
  $('.edit-icon').hide();
  $('#'+section).hide();
  $('#'+form).show();
}

function changePass() {
  $('#change-pass-btn').hide();
  $('#save-pass-btn').show();
  $('#password-form').show();
}

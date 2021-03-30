'use strict';

$(document).ready(function() {
  // チェックボックスのクリックを無効化します。
  $('.image_box .disabled_checkbox').click(function() {
    return false;
  });
	
  // 画像がクリックされた時の処理です。
  $('img.thumbnail').on('click', function() {
  	var this_id = $(this).prop('id');
    if (!$(this).is('.checked')) {
      // チェックが入っていない画像をクリックした場合、チェックを入れます。
      $(this).addClass('checked');
      $(this).next().prop('checked',true);
    } else {
      // チェックが入っている画像をクリックした場合、チェックを外します。
      $(this).removeClass('checked');
      $(this).next().prop('checked',false);
    }
  });
  $('img.thumbnail').on('reset', function() {
  	//リセット時、checkクラスをoffにする
  	$(this).removeClass('checked');
  	$(this).next().prop('checked',false);
  });
  $('#clear').click(function(){
  	$('img.thumbnail').removeClass('checked');
  	$('input:checkbox[name="categories[]"]').prop('checked',false);
  });
});
$(window).on('load',function(){
	$('input:checkbox[name="categories[]"]').prop('checked',false);
});
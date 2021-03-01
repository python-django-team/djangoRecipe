'use strict';

var VisionApiKey = 'AIzaSyDjE4Fytmz2rf7RgRY1C1fF-Y6U7j1oFN0';
var url = 'https://vision.googleapis.com/v1/images:annotate?key=';
var VisionApiUrl = url + VisionApiKey;

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

function clear() {
  $('#resultBox tr td').text("");
}
$('#uploader').change(function(evt) {
 
  getImageInfo(evt);
  clear();
  $(".resultArea").removeClass("hidden");
})

function getImageInfo(evt) {
  var file = evt.target.files;
  var reader = new FileReader();
  var dataUrl = "";
  reader.readAsDataURL(file[0]);
  reader.onload = function() {
    dataUrl = reader.result;
    $('#showPic').html("<img src='" + dataUrl + "'>");
    makeRequest(dataUrl, getVisionAPIInfo);
  }
}

function makeRequest(dataUrl, callback) {

  var end = dataUrl.indexOf(",")
  var request =  "{'requests': [{'image': {'content': '" + dataUrl.slice(end + 1) + "'},'features': [{'type': 'OBJECT_LOCALIZATION','maxResults': 4,}]}]}"
  callback(request)

}

function getVisionAPIInfo(request) {

  $.ajax({
    url: VisionApiUrl,
    type: 'POST',
    async: true,
    cache: false, 
    data: request,
    dataType: 'json',
    contentType: 'application/json',
  }).done(function(result) {
    showResult(result);
  }).fail(function(result) {
    console.log('failed to load info');
  });
}

function showResult(result) {
  for (var i = 0; i < result.responses[0].localizedObjectAnnotations.length; i++) {
    console.log(result.responses[0].localizedObjectAnnotations[i].name);
    $('#resultBox').append(`<tr><td class='resultTableContent'>${result.responses[0].localizedObjectAnnotations[i].name}</td></tr>`);
  }
}
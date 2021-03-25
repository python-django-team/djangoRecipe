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
    console.log("id");
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
  $('#checkboxes').text("");
  $('#recognition_to_search_button').addClass("hidden");
}
$('#uploader').change(function(evt) {
 
  getImageInfo(evt);
  clear();
  $(".ImageArea").removeClass("hidden");
  $(".resultArea").removeClass("hidden");
})

function getImageInfo(evt) {
  var file = evt.target.files;
  var reader = new FileReader();
  var dataUrl = "";
  console.log("why");
  reader.readAsDataURL(file[0]);
  reader.onload = function() {
    dataUrl = reader.result;
    $('#showPic').html("<img src='" + dataUrl + "'>");
    makeRequest(dataUrl, getVisionAPIInfo);
    /*
    var food_name_json_url = "static/json/food_name.json";
    $.getJSON(food_name_json_url, (data) => {
      var english_name = "Pork"
      if (data[english_name]) {
        console.log(data[english_name]);
        console.log(data[english_name][0]["japanese_name"]);
      }
      
    });
   */
    
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
  var food_name_json_url = "static/json/food_name.json";
  $.getJSON(food_name_json_url, (data) => {
    var english_name_array = result.responses[0].localizedObjectAnnotations.map((object) => object.name);
    console.log(english_name_array);
    var english_name_set = new Set(english_name_array);
    var flag = 0;

    english_name_set.forEach((english_name, index) => {
      console.log(english_name);
      if (data[english_name]) {
        var check_form = `
          <div class='custom-control custom-checkbox food_check'>
          <input type="checkbox" class='custom-control-input' name='categories[]' id='custom-check-${index}' value=${data[english_name][0]["id"]}>
          <label class='custom-control-label' for='custom-check-${index}'>${data[english_name][0]["japanese_name"]}</label>
          </div>`;
          $('#checkboxes').append($(check_form));
          flag = 1;
          var check_form2 = `
          <div class='custom-control custom-checkbox food_check'>
          <input type="checkbox" class='custom-control-input' name='categories[]' id='custom-check-0' value='10-276'>
          <label class='custom-control-label' for='custom-check-0'>豚肉</label>
          </div>`;
          $('#checkboxes').append($(check_form2));
      }
    })

    if (flag==1) {
      $('#recognition_to_search_button').removeClass("hidden");
    } else {
      var alert_message = `<div class="alert alert-danger" role="alert">
                          食材が一つも識別されませんでした
                          </div>`;
      $('.no_food').append($(alert_message));
    }

    
    /*
    for (var english_name of english_name_set) {
      if (data[english_name]) {

        $('#resultBox').append(`<tr><td class='resultTableContent'>${data[english_name][0]["japanese_name"]}</td></tr>`);
        var data = `
          <div class='custom-control custom-checkbox food_check'>
          <input type="checkbox" class='custom-control-input' id='custom-check-${}' value=${data[english_name][0]["id"]}>
          <label class='custom-control-label'>${data[english_name][0]["japanese_name"]}</label>
          </div>`;
      }
    }
    */
  });
}
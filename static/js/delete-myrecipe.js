d3 = document.getElementById("myrecipe_result");
d4 = document.getElementById("select-myrecipe-delete");

// デフォルト非表示
d4.style.display = "none";

function clickBtn3() {
    // 選択に変える
    d3.style.display = "none";
    d4.style.display = "block";
}

function clickBtn4() {
    // 戻す
    d4.style.display = "none";
    d3.style.display = "block";
}

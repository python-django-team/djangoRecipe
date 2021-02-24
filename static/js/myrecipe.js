d1 = document.getElementById("recipe_result");
d2 = document.getElementById("select-myrecipe");

// デフォルト非表示
d2.style.display = "none";

function clickBtn1() {
    // 選択に変える
    d1.style.display = "none";
    d2.style.display = "block";
}

function clickBtn2() {
    // 戻す
    d2.style.display = "none";
    d1.style.display = "block";
}

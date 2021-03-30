d1 = document.getElementById("recipe_result");
d2 = document.getElementById("select-myrecipe");
d3 = document.getElementById("myrecipe_result");
d4 = document.getElementById("select-myrecipe-delete");

// デフォルト非表示
d2.style.display = "none";
d4.style.display = "none";

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

async function callApi(){
  // 楽天レシピカテゴリ一覧API
  // const res = await fetch("https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=1008575362204726338&categoryType=large")
  // 楽天レシピカテゴリ別ランキングAPI
  // 大カテゴリ→categoryId=10 中カテゴリ→categoryId=10-276 小カテゴリ→categoryId=10-276-824
  // const res = await fetch("https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1008575362204726338&categoryId=10")
  const res = await fetch("https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1008575362204726338");
  
  // 使いやすい形に変換する
  const data = await res.json();
  console.log(data);
  console.log(data["result"][0]["recipeTitle"]);

  document.getElementById("data1").textContent=data["result"][0]["recipeTitle"];
  document.getElementById("data2").textContent=data["result"][1]["recipeTitle"]; 
  document.getElementById("data3").textContent=data["result"][2]["recipeTitle"]; 
  document.getElementById("data4").textContent=data["result"][3]["recipeTitle"];
}

callApi();
document.addEventListener("DOMContentLoaded", function () {
    const today = new Date(); // 現在の時刻を取得する
    today.setHours(0, 0, 0, 0); //比較の誤差を名無くすため、時刻をリセット

    document.querySelectorAll(".js-modal-open").forEach(function (item){ //　クラス .js-modal-open を持つ すべての要素 を取得→.forEach(function (item) { ... }); → 取得したすべての要素に対して、順番に処理を実行する。→itemに渡す
        const expireDateStr = item.getAttribute("data-expire-date");  //HTML の expire-date の値を取得する。
        if (expireDateStr) {
            const expireDate = new Date(expireDateStr);
            expireDate.setHours(0, 0, 0, 0); // 賞味期限の日付も 00:00:00 にリセット
            console.log("賞味期限: ", expireDate);  // 賞味期限をログに表示
            console.log("今日の日付: ", today);  // 今日の日付をログに表示

            if (expireDate < today) {
                item.classList.add("expired"); // CSSクラスを追加
                console.log("expired クラスを追加", item);  // クラスが追加されたか確認
            }
        }
    });
});

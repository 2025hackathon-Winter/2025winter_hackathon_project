document.addEventListener("DOMContentLoaded", function () {
    // ソートボタンの取得
    const sortByNextPurchaseDate = document.getElementById("sort-next-purchase");
    const sortByPurchaseDate = document.getElementById("sort-recent-purchase");

    if (!sortByNextPurchaseDate || !sortByPurchaseDate) {
        console.error("ソートボタンが見つかりません");
        return;
    }

    let isAscending = true; // 昇順・降順の状態を管理

    // ソート関数
    function sortItems(containerId, sortKey) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const items = Array.from(container.getElementsByClassName("item"));

        items.sort((a, b) => {
            const aElement = a.querySelector(`[data-key="${sortKey}"]`);
            const bElement = b.querySelector(`[data-key="${sortKey}"]`);

            if (!aElement || !bElement) {
                console.warn(`要素が見つかりません: ${sortKey}`);
                return 0;
            }

            // 不要な文字列を削除して日付部分のみ取得
            const aText = aElement.textContent.trim().replace(/[^0-9/]/g, '');
            const bText = bElement.textContent.trim().replace(/[^0-9/]/g, '');

            console.log("Cleaned Text → aText:", aText, "bText:", bText);

            if (!aText || !bText) return 0; // 値がない場合は並べ替えしない

            const aValue = new Date(aText);
            const bValue = new Date(bText);

            return isAscending ? aValue - bValue : bValue - aValue; // 昇順・降順を切り替え
        });

        items.forEach(item => container.appendChild(item));
    }

    // 「次回購入期限順」ボタン
    sortByNextPurchaseDate.addEventListener("click", function () {
        isAscending = !isAscending; // 昇順・降順を切り替える
        sortItems("all-content", "next_purchase_date");
        sortItems("daily-content", "next_purchase_date");
        sortItems("food-content", "next_purchase_date");
        sortItems("others-content", "next_purchase_date");
    });

    // 「最近買った順」ボタン
    sortByPurchaseDate.addEventListener("click", function () {
        isAscending = !isAscending; // 昇順・降順を切り替える
        sortItems("all-content", "purchase_date");
        sortItems("daily-content", "purchase_date");
        sortItems("food-content", "purchase_date");
        sortItems("others-content", "purchase_date");
    });
});
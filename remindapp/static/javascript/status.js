// document.addEventListener("DOMContentLoaded", function() {
//         const nextPurchaseDate = "{{ goods.next_purchase_date|date:'Y-m-d' }}"; // 商品ごとの次回購入予定日
//         const currentDate = new Date(); // 現在の日付
//         const targetDate = new Date(nextPurchaseDate); // 次回購入予定日

//         // 1週間前の日付を計算
//         const oneWeekBefore = new Date(targetDate);
//         oneWeekBefore.setDate(targetDate.getDate() - 7);

//         // 商品ごとの「〇」の色を設定
//         const purchaseStatusElement = document.getElementById('purchase-status-{{ goods.id }}');

//         // デバッグ：purchaseStatusElementがnullではないか確認
//         console.log(purchaseStatusElement);

//         if (purchaseStatusElement) {
//             // 色を決定
//             if (currentDate > targetDate) {
//                 // 期限を過ぎている場合は赤
//                 purchaseStatusElement.style.color = "red";
//             } else if (currentDate > oneWeekBefore) {
//                 // 1週間以内の場合はオレンジ
//                 purchaseStatusElement.style.color = "orange";
//             } else {
//                 // それ以外は緑
//                 purchaseStatusElement.style.color = "green";
//             }
//         } else {
//             console.error("要素が見つかりません:", 'purchase-status-{{ goods.id }}');
//         }
// });
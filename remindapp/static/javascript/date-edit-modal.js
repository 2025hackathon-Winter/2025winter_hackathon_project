document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".modal").forEach(function (modal) { //modalクラスの要素を全て取得し、それぞれに対して処理する
        const editButton = modal.querySelector(".edit-button");   //各モーダル内の要素を取得し、変数に格納する。
        const saveButton = modal.querySelector(".save-button");
        const displayMode = modal.querySelector(".display-mode");
        const editMode = modal.querySelector(".edit-mode");

        const purchaseDate = modal.querySelector(".purchase-date");
        const expireDate = modal.querySelector(".expire-date");
        const nextPurchaseDate = modal.querySelector(".next-purchase-date");
        const nextPurchaseTerm = modal.querySelector(".next-purchase-term");

        const inputPurchaseDate = modal.querySelector(".input-purchase-date");
        const inputExpireDate = modal.querySelector(".input-expire-date");
        const inputNextPurchaseDate = modal.querySelector(".input-next-purchase-date");
        const inputNextPurchaseTerm = modal.querySelector(".input-next-purchase-term");

        // 編集ボタンをクリックで入力モードに切り替え
        editButton.addEventListener("click", function () { //.edit-buttonを選択した際に、表示を無くす。
            displayMode.style.display = "none";
            editMode.style.display = "block";
            editButton.style.display = "none";
            saveButton.style.display = "inline-block";
        });

        // 保存ボタンをクリックでデータ送信
        saveButton.addEventListener("click", function () {  //.save-button をクリックすると、入力された情報をサーバーに送信。
            const goodsId = modal.id.replace("all-modal-", ""); // モーダルのIDから goods.id を取得

            const updatedData = {
                id: goodsId,
                purchase_date: inputPurchaseDate.value,
                expire_date: inputExpireDate.value,
                next_purchase_date: inputNextPurchaseDate.value,
                next_purchase_term: inputNextPurchaseTerm.value,
            };

            fetch("/update_goods/", {  //fetch を使って サーバーのエンドポイント /update_goods/(←バックエンドに要確認) にデータを送信
                method: "POST",
                headers: {
                    "Content-Type": "application/json", // データの形式が JSON であることを指定する。
                    "X-CSRFToken": getCSRFToken(), // CSRFトークンを取得
                },
                body: JSON.stringify(updatedData),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 更新成功時、表示に反映
                    purchaseDate.textContent = inputPurchaseDate.value;
                    expireDate.textContent = inputExpireDate.value;
                    nextPurchaseDate.textContent = inputNextPurchaseDate.value;
                    nextPurchaseTerm.textContent = inputNextPurchaseTerm.value;

                    displayMode.style.display = "block";
                    editMode.style.display = "none";
                    editButton.style.display = "inline-block";
                    saveButton.style.display = "none";
                } else {
                    alert("更新に失敗しました");
                }
            })
            .catch(error => console.error("エラー:", error));
        });

        function getCSRFToken() {
            const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            return csrfTokenElement ? csrfTokenElement.value : "";
        }
    });
});
// document.addEventListener('DOMContentLoaded', function(){
//     //要素を取得 今回はhtmlのidで要素を取得する
//     const modal = document.querySelector('.js-modal'),
//         open = document.querySelector('.js-modal-open'),
//         close = document.querySelector('.js-modal-close');

//     //modal要素のclassに'is-active'を追加　CSSでモーダルを表示させる。
//     function modalOpen() {
//         modal.classList.add('is-active');
//     }
//     //クリックしたときに、modalOpen()を実行する。open(クリック対象の要素)→イベント登録メゾット→click(イベント発火)→実行される関数
//     open.addEventListener('click', modalOpen);

//     function modalClose() {
//         modal.classList.remove('is-active');
//     }
//     close.addEventListener('click', modalClose);

//     function modalOut(e) {
//         if (e.target === modal) {
//             modal.classList.remove('is-active');
//         }
//     }
//     modal.addEventListener('click', modalOut);
// });

// ↓↓↓↓モーダル毎にターゲットを変えないと表示されない

document.addEventListener('DOMContentLoaded', function () {
    // すべての「開く」ボタンを取得
    const openButtons = document.querySelectorAll('.js-modal-open');

    openButtons.forEach(button => {
        button.addEventListener('click', function () {
            // data-target属性から対応するモーダルIDを取得
            const modalId = button.getAttribute('data-target');
            const modal = document.getElementById(modalId);

            if (modal) {
                modal.classList.add('is-active'); // モーダルを開く
                const close = modal.querySelector('.js-modal-close'); // 閉じるボタン

                // モーダルを閉じる関数
                function modalClose() {
                    modal.classList.remove('is-active');
                }

                close.addEventListener('click', modalClose);

                modal.addEventListener('click', function (e) {
                    if (e.target === modal) {
                        modalClose();
                    }
                });
            }
        });
    });
});

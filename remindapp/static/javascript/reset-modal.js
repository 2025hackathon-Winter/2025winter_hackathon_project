document.addEventListener('DOMContentLoaded', function(){
    //要素を取得 今回はhtmlのidで要素を取得する
    const modal = document.querySelector('#js-reset-modal'),
        open = document.querySelector('#js-reset-modal-open'),
        close = document.querySelector('#js-reset-modal-close');

    //modal要素のclassに'is-active'を追加　CSSでモーダルを表示させる。
    function modalOpen() {
        modal.classList.add('is-active');
    }
    //クリックしたときに、modalOpen()を実行する。open(クリック対象の要素)→イベント登録メゾット→click(イベント発火)→実行される関数
    open.addEventListener('click', modalOpen);

    function modalClose() {
        modal.classList.remove('is-active');
    }
    close.addEventListener('click', modalClose);

    function modalOut(e) {
        if (e.target === modal) {
            modal.classList.remove('is-active');
        }
    }
    modal.addEventListener('click', modalOut);
});
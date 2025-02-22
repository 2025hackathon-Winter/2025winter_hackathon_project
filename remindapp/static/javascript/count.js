
// 4行目はhtmlが読み込まれたら関数を発火するようにする

document.addEventListener('DOMContentLoaded', function(){
    const countElement = document.querySelector('.count');
    const inputElement = document.querySelector('input[name="default_term"]'); // フォームの入力要素 : MANA追記
    const increment = document.querySelector('#js-increment');
    const decrement = document.querySelector('#js-decrement');

    let count = parseInt(inputElement.value, 10) || 0;  // 初期値を `input` の値から取得 : MANA追記

    // クリックするとカウントが１追加される
    increment.addEventListener('click', function() {
        count++;
        updateCount();
    });

    // クリックするとカウントが１減少する
    decrement.addEventListener('click', function() {
        if (count > 0){
            count--;
            updateCount();
        }
    });

    function updateCount(){
        countElement.textContent = count;
        inputElement.value = count; // `input` の値も更新（バックエンドへ送信される）: MANA追記
    }
});


// 4行目はhtmlが読み込まれたら関数を発火するようにする

document.addEventListener('DOMContentLoaded', function(){
    const countElement = document.querySelector('.count');
    const increment = document.querySelector('#js-increment');
    const decrement = document.querySelector('#js-decrement');

    let count = 0;

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
    }
});

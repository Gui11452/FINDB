(function(){

    const b1 = document.querySelector('.btn-tres-meses');
    const b2 = document.querySelector('.btn-doze-meses');
    const b3 = document.querySelector('.btn-seis-meses');
    const l1 = document.querySelector('.loader-tres-meses');
    const l2 = document.querySelector('.loader-doze-meses');
    const l3 = document.querySelector('.loader-seis-meses');

    document.addEventListener('click', e => {
        const el = e.target;
        if(el == b1){
            l1.style.display = 'flex';
        } else if(el == b2){
            l2.style.display = 'flex';
        } else if(el == b3){
            l3.style.display = 'flex';
        }

        if(el == b1 || el == b2 || el == b3){
            if(b1){
                b1.style.display = 'none';
            }
            if(b2){
                b2.style.display = 'none';
            }
            if(b3){
                b3.style.display = 'none';
            }
        } 

    });

})();
(function(){
    const banner1I = document.querySelector('#banner1 ~ label>i');
    const banner2I = document.querySelector('#banner2 ~ label>i');
    const banner3I = document.querySelector('#banner3 ~ label>i');
    const carroselInterno = document.querySelector('.carrosel-interno>div');

    document.addEventListener('click', e => {
        const el = e.target;

        // Os transform translate desloca a partir da sua posição original

        if(el == banner1I){
            if(carroselInterno.classList.contains('rolagem-right-1') &&
                carroselInterno.classList.contains('rolagem-right-2')){
                carroselInterno.classList.remove('rolagem-right-1'); 
                carroselInterno.classList.remove('rolagem-right-2'); 
            }
            else if(carroselInterno.classList.contains('rolagem-right-2')){
                carroselInterno.classList.remove('rolagem-right-2');
            } 
            else if(carroselInterno.classList.contains('rolagem-right-1')){
                carroselInterno.classList.remove('rolagem-right-1'); 
            }

            if(banner1I){
                banner1I.classList.add('azul');
            }
            if(banner2I){
                banner2I.classList.remove('azul');
            }
            if(banner3I){
                banner3I.classList.remove('azul');
            }
        }
        else if(el == banner2I){
            if(carroselInterno.classList.contains('rolagem-right-1') &&
            carroselInterno.classList.contains('rolagem-right-2')){
                carroselInterno.classList.remove('rolagem-right-2');
            } else if(carroselInterno.classList.contains('rolagem-right-2')){
                carroselInterno.classList.remove('rolagem-right-2');
                carroselInterno.classList.add('rolagem-right-1');
            } else{
                carroselInterno.classList.add('rolagem-right-1');
            }

            if(banner1I){
                banner1I.classList.remove('azul');
            }
            if(banner2I){
                banner2I.classList.add('azul');
            }
            if(banner3I){
                banner3I.classList.remove('azul');
            }

        }

        else if(el == banner3I){
            if(carroselInterno.classList.contains('rolagem-right-1') &&
            carroselInterno.classList.contains('rolagem-right-2')){
                
            } else if(carroselInterno.classList.contains('rolagem-right-1')){
                carroselInterno.classList.add('rolagem-right-2');
            } else{
                carroselInterno.classList.add('rolagem-right-2');
            }

            if(banner1I){
                banner1I.classList.remove('azul');
            }
            if(banner2I){
                banner2I.classList.remove('azul');
            }
            if(banner3I){
                banner3I.classList.add('azul');
            }
        }

    });

    let count = 1;
    setInterval(function(){
        if(count == 0){
            if(banner1I){
                banner1I.click();
            } else if(banner2I){
                banner2I.click();
            } else if(banner3I){
                banner3I.click();
            }
        } else if(count == 1){
            if(banner2I){
                banner2I.click();
            } else if(banner3I){
                banner3I.click();
            } else if(banner1I){
                banner1I.click();
            }
        } else if(count == 2){
            if(banner3I){
                banner3I.click();
            } else if(banner1I){
                banner1I.click();
            } else if(banner2I){
                banner2I.click();
            }
        } else{
            count = 0;
            if(banner1I){
                banner1I.click();
            } else if(banner2I){
                banner2I.click();
            } else if(banner3I){
                banner3I.click();
            }
        }
        count++;
    }, 10000);

})();
(function(){

    const pessoasDiv = document.querySelectorAll('.pessoa>div');
    const botoesConvidarChamada = document.querySelectorAll('.convidar-video');
    const botoesConvidarChamadaI = document.querySelectorAll('.convidar-video i');
    const botoesFecharConvidarChamada = document.querySelectorAll('.box-convidar-video>i');

    const buttonConvidar = document.querySelectorAll('.pessoa>button');
    const buttonConvidarI = document.querySelectorAll('.pessoa>button i');
    const pessoaDropdown = document.querySelectorAll('.pessoa .dropdown');

    const loader = document.querySelector('.loader');
    const botaoSubmit = document.querySelector('#submit');
    const formConvidarAmigos = document.querySelector('#form-convidar-amigos');
    
    const loaderBoxConvidarVideo = document.querySelectorAll('.loader-box-convidar-video');
    const formBoxConvidarVideo = document.querySelectorAll('.form-box-convidar-video');
    const submitFormBoxConvidarVideo = document.querySelectorAll('.submit-form-box-convidar-video');

    const carrosselIMG = document.querySelectorAll('.carrosel-interno img');
    for(let cImg = 0; cImg < carrosselIMG.length; cImg++){
        if(carrosselIMG[cImg].getAttribute('link') != 'None'){
            carrosselIMG[cImg].classList.add('selecionado');
        }
    }

    document.addEventListener('click', e => {

        const el = e.target;
        for(let bC = 0; bC < botoesConvidarChamada.length; bC++){
            if(el == botoesConvidarChamada[bC]|| el == botoesConvidarChamadaI[bC]){
                e.preventDefault();
                pessoasDiv[bC].style.display = 'flex';
                break;
            }
        }

        for(let bF = 0; bF < botoesFecharConvidarChamada.length; bF++){
            if(el == botoesFecharConvidarChamada[bF]){
                e.preventDefault();
                pessoasDiv[bF].style.display = 'none';
                break;
            }
        }

        for(let cImg = 0; cImg < carrosselIMG.length; cImg++){
            if(el == carrosselIMG[cImg] && carrosselIMG[cImg].getAttribute('link') != 'None'){
                let link = carrosselIMG[cImg].getAttribute('link');
                window.open(link);
            }
        }

        for(let bDC = 0; bDC < buttonConvidar.length; bDC++){
            if(el == buttonConvidar[bDC] || el == buttonConvidarI[bDC]){
                e.preventDefault();
                pessoaDropdown[bDC].classList.toggle('dropdown-desocultar');
                break;
            }
        }

    });

    document.addEventListener('submit', e => {
        const el = e.target;
        
        if(el == formConvidarAmigos){
            loader.style.display = 'inline-block';
            botaoSubmit.style.display = 'none';
            return;
        }

        for(let i = 0; i < formBoxConvidarVideo.length; i++){
            if(el == formBoxConvidarVideo[i]){
                loaderBoxConvidarVideo[i].style.display = 'inline-block';
                submitFormBoxConvidarVideo[i].style.display = 'none';
                return;
            }
        }
        
    });


})();
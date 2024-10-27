(function(){

    const pessoasDiv = document.querySelectorAll('.cupido div.box-chamada-video');
    const botoesConvidarChamada = document.querySelectorAll('.convidar-video');
    const botoesConvidarChamadaI = document.querySelectorAll('.convidar-video i');
    const botoesFecharConvidarChamada = document.querySelectorAll('.box-convidar-video>i');

    const loaderBoxConvidarVideo = document.querySelectorAll('.loader-box-convidar-video');
    const formBoxConvidarVideo = document.querySelectorAll('.form-box-convidar-video');
    const submitFormBoxConvidarVideo = document.querySelectorAll('.submit-form-box-convidar-video');

    const buttonConvidar = document.querySelectorAll('.cupido>button');
    const buttonConvidarI = document.querySelectorAll('.cupido>button i');
    const cupidoDropdown = document.querySelectorAll('.cupido .dropdown');

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

        for(let bDC = 0; bDC < buttonConvidar.length; bDC++){
            if(el == buttonConvidar[bDC] || el == buttonConvidarI[bDC]){
                e.preventDefault();
                cupidoDropdown[bDC].classList.toggle('dropdown-desocultar');
                break;
            }
        }

    });

    document.addEventListener('submit', e => {
        const el = e.target;

        for(let i = 0; i < formBoxConvidarVideo.length; i++){
            if(el == formBoxConvidarVideo[i]){
                loaderBoxConvidarVideo[i].style.display = 'inline-block';
                submitFormBoxConvidarVideo[i].style.display = 'none';
                return;
            }
        }
        
    });

})();
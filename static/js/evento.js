(function(){

    const pessoasDiv = document.querySelectorAll('.participante div.box-chamada-video');
    const botoesConvidarChamada = document.querySelectorAll('.convidar-video');
    const botoesConvidarChamadaI = document.querySelectorAll('.convidar-video i');
    const botoesFecharConvidarChamada = document.querySelectorAll('.box-convidar-video>i');

    const loaderParticipanteChamadaVideo = document.querySelectorAll('.loader-participante-chamada-video');
    const formParticipanteChamadaVideo = document.querySelectorAll('.form-participante-chamada-video');
    const submitFormParticipanteChamadaVideo = document.querySelectorAll('.submit-form-participante-chamada-video');

    const btnConfirmarEvento = document.querySelector('.confirmar-evento');
    const loaderConfirmarEvento = document.querySelector('.loader-confirmar-evento');
    const formEvento = document.querySelector('.evento');

    const perguntaH3 = document.querySelectorAll('.pergunta h3');
    const perguntaH3IPlus = document.querySelectorAll('.pergunta h3 i.fa-plus');
    const perguntaH3IMinus = document.querySelectorAll('.pergunta h3 i.fa-minus');
    const perguntaP = document.querySelectorAll('.pergunta p');

    document.addEventListener('click', e => {

        const el = e.target;

        for(let p = 0; p < perguntaH3.length; p++){
            if(el == perguntaH3[p]){
                perguntaH3IPlus[p].classList.toggle('ocultar');
                perguntaH3IMinus[p].classList.toggle('desocultar');
                perguntaP[p].classList.toggle('desocultar');
                
                for(let p2 = 0; p2 < perguntaH3.length; p2++){
                    if(p != p2){
                        perguntaH3IPlus[p2].classList.remove('ocultar');
                        perguntaH3IMinus[p2].classList.remove('desocultar');
                        perguntaP[p2].classList.remove('desocultar');
                    }
                }
    
            }
        }

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

    });

    document.addEventListener('submit', e => {
        const el = e.target;

        if(el == formEvento){
            loaderConfirmarEvento.style.display = 'inline-block';
            btnConfirmarEvento.style.display = 'none';
            return;
        }

        for(let i = 0; i < formParticipanteChamadaVideo.length; i++){
            if(el == formParticipanteChamadaVideo[i]){
                loaderParticipanteChamadaVideo[i].style.display = 'inline-block';
                submitFormParticipanteChamadaVideo[i].style.display = 'none';
                return;
            }
        }
        
    });

})();
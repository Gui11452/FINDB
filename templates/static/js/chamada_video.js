(function(){

    const btnConfirmarChamada = document.querySelector('.btn-confirmar-chamada');
    const btnRejeitarChamada = document.querySelector('.btn-rejeitar-chamada');
    const loaderBotoes = document.querySelector('.loader-botoes');

    document.addEventListener('click', e => {

        const el = e.target;

        if(el == btnConfirmarChamada){
            btnConfirmarChamada.style.display = 'none';
            loaderBotoes.style.display = 'inline-block';
        } else if(el == btnRejeitarChamada){
            btnRejeitarChamada.style.display = 'none';
            loaderBotoes.style.display = 'inline-block';
        }


    });

})();
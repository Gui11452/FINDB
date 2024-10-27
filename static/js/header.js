(function(){

    const barraNotificacoes = document.querySelectorAll('.barra-notificacoes');
    const [b1, b2] = barraNotificacoes;
    const barraNotificacoesI = document.querySelectorAll('.barra-notificacoes i');
    const [bI1, bI2] = barraNotificacoesI;
    const barraNotificacoesSpan = document.querySelectorAll('.barra-notificacoes span');
    const [bSpan1, bSpan2] = barraNotificacoesSpan;

    const boxNotificacoes = document.querySelector('.box-notificacoes');
    const boxNotificacoesI = document.querySelector('.box-notificacoes>div>i');

    document.addEventListener('click', e => {
        const el = e.target;
        if(el == b1 || el == b2 || el == bI1 || el == bI2 || el == bSpan1 || el == bSpan2){
            boxNotificacoes.style.display = 'flex';
        } else if(el == boxNotificacoesI){
            boxNotificacoes.style.display = 'none';
        }

    });

})();
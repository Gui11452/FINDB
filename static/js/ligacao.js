(function(){

    const mensagemLigacao = document.querySelector('.mensagem-ligacao');
    const buttonMensagemLigacao = document.querySelector('.mensagem-ligacao button');

	const nomeVariavel = localStorage.getItem('mensagemLigacao');
	const elementoJS = JSON.parse(nomeVariavel);
    if(!elementoJS){
        setTimeout(() => {
            mensagemLigacao.style.display = 'flex';
            const elementoJSON = JSON.stringify(true);
	        localStorage.setItem('mensagemLigacao', elementoJSON)
        }, 1000);
    }

    document.addEventListener('click', e => {

        const el = e.target;

        if(el == buttonMensagemLigacao){
            mensagemLigacao.style.display = 'none';
            return;
        }

    });

})();
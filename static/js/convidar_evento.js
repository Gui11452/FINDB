(function(){

    const descricao = document.querySelectorAll('.descricao');
    const pDescricao = document.querySelectorAll('.p-descricao');

    const loaderEvento = document.querySelectorAll('.loader-evento');
    const formEvento = document.querySelectorAll('.evento');
    const submitFormEvento = document.querySelectorAll('.btn-evento');

    document.addEventListener('submit', e => {

        const el = e.target;

        for(let i = 0; i < formEvento.length; i++){
            if(el == formEvento[i]){
                loaderEvento[i].style.display = 'inline-block';
                submitFormEvento[i].style.display = 'none';
                return;
            }
        }
        

    });

    document.addEventListener('input', e => {

        const el = e.target;
        
        for(let i = 0; i < descricao.length; i++){
            if(el == descricao[i]){
                if(descricao[i].value.length <= 2000){
                    pDescricao[i].innerHTML = `Descrição: ${descricao[i].value.length}/2000 caracteres escritos`
                }
            }
        }

    });

})();
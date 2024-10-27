(function(){

    const botaoAbrirFiltro = document.querySelector('#botao-filtro');
    const botaoAbrirFiltroI = document.querySelector('#botao-filtro i');
    const botaoFecharFiltro = document.querySelector('#form-inputs h2 i');

    const filtroOculto = document.querySelector('#form-inputs');

    const loader = document.querySelector('.loader');
    const botaoFiltrar = document.querySelector('#filtrar');

    const nome = document.querySelector('#nome');
    const genero = document.querySelector('#genero');
    const idade = document.querySelector('#idade');

    const usuario = document.querySelector('#usuario');

    const data = document.querySelector('#data');

    const nacionalidade = document.querySelector('#nacionalidade');
    const email = document.querySelector('#email');

    const pais = document.querySelector('#pais');

    const regiao = document.querySelector('#regiao');

    const orientacaoSexual = document.querySelector('#orientacao_sexual');

    const estadoCivil = document.querySelector('#estado_civil');
    const signo = document.querySelector('#signo');

    const etnia = document.querySelector('#etnia');
    const corCabelo = document.querySelector('#cor_cabelo');

    const corOlhos = document.querySelector('#cor_olhos');
    const altura = document.querySelector('#altura');

    const bebe = document.querySelector('#bebe');

    const tipoCorpo = document.querySelector('#tipo_corpo');
    const fuma = document.querySelector('#fuma');

    const descricao = document.querySelector('#descricao');

    const requestGET = document.querySelector('#request-get');

    const pessoasDiv = document.querySelectorAll('.filtro div.box-chamada-video');
    const botoesConvidarChamada = document.querySelectorAll('.convidar-video');
    const botoesConvidarChamadaI = document.querySelectorAll('.convidar-video i');
    const botoesFecharConvidarChamada = document.querySelectorAll('.box-convidar-video>i');

    const formFiltro = document.querySelector('#form-filtro');

    const loaderBoxConvidarVideo = document.querySelectorAll('.loader-box-convidar-video');
    const formBoxConvidarVideo = document.querySelectorAll('.form-box-convidar-video');
    const submitFormBoxConvidarVideo = document.querySelectorAll('.submit-form-box-convidar-video');

    const buttonConvidar = document.querySelectorAll('.filtro>div>button');
    const buttonConvidarI = document.querySelectorAll('.filtro>div>button i');
    const filtroDropdown = document.querySelectorAll('.filtro .dropdown');

    function botadadosRequestGET(){
        let dadosRequestGET = requestGET.getAttribute('request_get');
        dadosRequestGET = dadosRequestGET.replace('<QueryDict: ', '').replace('>', '').replace(/'/g, '"');
        dadosRequestGET = JSON.parse(dadosRequestGET);
        
        if(dadosRequestGET.nome){nome.value = dadosRequestGET.nome;}
        if(dadosRequestGET.idade){idade.value = dadosRequestGET.idade;}
        //if(dadosRequestGET.genero){genero.value = dadosRequestGET.genero;}
        if(dadosRequestGET.data){data.value = dadosRequestGET.data;}
        if(dadosRequestGET.nacionalidade){nacionalidade.value = dadosRequestGET.nacionalidade;}
        if(dadosRequestGET.email){email.value = dadosRequestGET.email;}
        if(dadosRequestGET.pais){pais.value = dadosRequestGET.pais;}
        //if(dadosRequestGET.orientacao_sexual){orientacaoSexual.value = dadosRequestGET.orientacao_sexual;}
        if(dadosRequestGET.regiao){regiao.value = dadosRequestGET.regiao;}
        if(dadosRequestGET.estadoCivil){estadoCivil.value = dadosRequestGET.estadoCivil;}
        if(dadosRequestGET.signo){signo.value = dadosRequestGET.signo;}
        if(dadosRequestGET.etnia){etnia.value = dadosRequestGET.etnia;}
        if(dadosRequestGET.cor_cabelo){corCabelo.value = dadosRequestGET.cor_cabelo;}
        if(dadosRequestGET.cor_olhos){corOlhos.value = dadosRequestGET.cor_olhos;}
        if(dadosRequestGET.altura){altura.value = dadosRequestGET.altura;}
        if(dadosRequestGET.bebe){bebe.value = dadosRequestGET.bebe;}
        if(dadosRequestGET.tipo_corpo){tipoCorpo.value = dadosRequestGET.tipo_corpo;}
        if(dadosRequestGET.fuma){fuma.value = dadosRequestGET.fuma;}
        if(dadosRequestGET.descricao){descricao.value = dadosRequestGET.descricao;}
    }
    botadadosRequestGET();

    document.addEventListener('click', e => {

        const el = e.target;

        if(el == botaoAbrirFiltro || el == botaoAbrirFiltroI){
            e.preventDefault();
            filtroOculto.style.display = 'flex';
        } else if(el == botaoFecharFiltro){
            e.preventDefault();
            filtroOculto.style.display = 'none';
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

        for(let bDC = 0; bDC < buttonConvidar.length; bDC++){
            if(el == buttonConvidar[bDC] || el == buttonConvidarI[bDC]){
                e.preventDefault();
                filtroDropdown[bDC].classList.toggle('dropdown-desocultar');
                break;
            }
        }

    });

    document.addEventListener('submit', e => {
        const el = e.target;

        if(el == formFiltro){
            loader.style.display = 'inline-block';
            botaoFiltrar.style.display = 'none';
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
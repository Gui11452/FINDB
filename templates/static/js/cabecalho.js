const botaoMobile = document.querySelector('.botao-mobile');
const botaoMobileSpan = document.querySelectorAll('.botao-mobile span');
const [span1, span2, span3] = botaoMobileSpan;

/* const popup = document.querySelector('.popup');
const popupI = document.querySelector('.popup i'); */

const botaoOculto = document.querySelector('.botao-oculto');
const botaoOcultoSpan = document.querySelectorAll('.botao-oculto span');
const [span4, span5] = botaoOcultoSpan;

const cabecalhoMobile = document.querySelector('.cabecalho-mobile');

document.addEventListener('click', e => {

    const el = e.target;

    /* if(el == popupI){
        popup.style.display = 'none';
    } */

    if(el == span1 || el == span2 || el == span3 || el == botaoMobile){
        cabecalhoMobile.classList.add('desocultar-menu');
        botaoOculto.style.display = 'flex'; 
        botaoMobile.style.display = 'none';
    } else if(el == span4 || el == span5 || el == botaoOculto){
        cabecalhoMobile.classList.remove('desocultar-menu');
        botaoOculto.style.display = 'none';
        botaoMobile.style.display = 'flex';
    }

});


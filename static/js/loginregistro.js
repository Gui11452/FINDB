const container = document.querySelector('.container');
let o = 0;
let p = 1;
function opacidade(){
    let interval = setInterval(function(){
        if(o >= 0.7){
            if(p >= 5){
                p = 1;
                o=0;
            } else {
                p+=1;
                o=0;
            }
            container.setAttribute('style', `background: linear-gradient(rgba(255, 255, 255, ${o}), rgba(255, 255, 255, ${o})), url('/static/images/pessoas${p}.jpg') center; background-size: cover;`);
            iniciarIntervalo();
            clearInterval(interval);
        } else{
            o+=0.01;
            container.setAttribute('style', `background: linear-gradient(rgba(255, 255, 255, ${o}), rgba(255, 255, 255, ${o})), url('/static/images/pessoas${p}.jpg') center; background-size: cover;`);
        }
    }, 1);
}

function iniciarIntervalo(){
    setTimeout(function(){
        opacidade();
    }, 3000);
};

iniciarIntervalo();
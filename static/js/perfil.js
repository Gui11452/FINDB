(function(){

    const btnAddAlbum = document.querySelector('#btn-add-album');
    const loader = document.querySelector('.loader');
    const btnGerenciarAlbum = document.querySelector('#gerenciar-album');

    const albumForm = document.querySelector('#album form');

    const pessoaDiv = document.querySelector('.perfil div.box-chamada-video');
    const botoesConvidarChamada = document.querySelector('.convidar-video');
    const botoesConvidarChamadaI = document.querySelector('.convidar-video i');
    const botoesFecharConvidarChamada = document.querySelector('.box-convidar-video>i');

    const albumFiltro = document.querySelector('#form-album');

    const loaderBoxConvidarVideo = document.querySelector('.loader-box-convidar-video');
    const formBoxConvidarVideo = document.querySelector('.form-box-convidar-video');
    const submitFormBoxConvidarVideo = document.querySelector('.submit-form-box-convidar-video');

    document.addEventListener('click', e => {

        const el = e.target;

        if(el == btnAddAlbum){
            e.preventDefault();
            albumForm.classList.toggle('desocultado');
        }

        if(el == botoesConvidarChamada || el == botoesConvidarChamadaI){
            e.preventDefault();
            pessoaDiv.style.display = 'flex';
        }

        if(el == botoesFecharConvidarChamada){
            e.preventDefault();
            pessoaDiv.style.display = 'none';
        }

    });

    document.addEventListener('submit', e => {
        const el = e.target;

        if(el == albumFiltro){
            loader.style.display = 'inline-block';
            btnGerenciarAlbum.style.display = 'none';
            return;
        }

        if(el == formBoxConvidarVideo){
            loaderBoxConvidarVideo.style.display = 'inline-block';
            submitFormBoxConvidarVideo.style.display = 'none';
            return;
        }
        
    });

})();
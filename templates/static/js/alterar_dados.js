(function(){

    // Inputs
    const nome = document.querySelector('#nome');
    const genero = document.querySelector('#genero');
    //const usuario = document.querySelector('#usuario');
    const data = document.querySelector('#data');
    const nacionalidade = document.querySelector('#nacionalidade');
    const email = document.querySelector('#email');
    const pais = document.querySelector('#pais');
    const celular = document.querySelector('#celular');
    const regiao = document.querySelector('#regiao');
    const interesses = document.querySelector('#interesses');
    const orientacaoSexual = document.querySelector('#orientacao_sexual');
    const profissao = document.querySelector('#profissao');
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
    const pDescricao = document.querySelector('.p-descricao');
    const foto = document.querySelector('#foto');

    // Checkbox
    const checkboxNome = document.querySelector('#checkbox-nome');
    const checkboxGenero = document.querySelector('#checkbox-genero');
    const checkboxData = document.querySelector('#checkbox-data');
    const checkboxNacionalidade = document.querySelector('#checkbox-nacionalidade');
    const checkboxEmail = document.querySelector('#checkbox-email');
    const checkboxPais = document.querySelector('#checkbox-pais');
    const checkboxCelular = document.querySelector('#checkbox-celular');
    const checkboxRegiao = document.querySelector('#checkbox-regiao');
    const checkboxInteresses = document.querySelector('#checkbox-interesses');
    const checkboxOrientacaoSexual = document.querySelector('#checkbox-orientacao-sexual');
    const checkboxProfissao = document.querySelector('#checkbox-profissao');
    const checkboxEstadoCivil = document.querySelector('#checkbox-estado-civil');
    const checkboxSigno = document.querySelector('#checkbox-signo');
    const checkboxEtnia = document.querySelector('#checkbox-etnia');
    const checkboxCorCabelo = document.querySelector('#checkbox-cor-cabelo');
    const checkboxCorOlhos = document.querySelector('#checkbox-cor-olhos');
    const checkboxAltura = document.querySelector('#checkbox-altura');
    const checkboxBebe = document.querySelector('#checkbox-bebe');
    const checkboxTipoCorpo = document.querySelector('#checkbox-tipo-corpo');
    const checkboxFuma = document.querySelector('#checkbox-fuma');
    const checkboxDescricao = document.querySelector('#checkbox-descricao');
    const checkboxFoto = document.querySelector('#checkbox-foto');

    // Errors
    const errorNome = document.querySelector('#error_nome');
    //const errorUsuario = document.querySelector('#error_usuario');
    const errorGenero = document.querySelector('#error_genero');
    const errorData = document.querySelector('#error_data');
    const errorNacionalidade = document.querySelector('#error_nacionalidade');
    const errorEmail = document.querySelector('#error_email');
    const errorPais = document.querySelector('#error_pais');
    const errorCelular = document.querySelector('#error_celular');
    const errorRegiao = document.querySelector('#error_regiao');
    const errorInteresses = document.querySelector('#error_interesses');
    const errorOrientacaoSexual = document.querySelector('#error_orientacao_sexual');
    const errorProfissao = document.querySelector('#error_profissao');
    const errorEstadoCivil = document.querySelector('#error_estado_civil');
    const errorSigno = document.querySelector('#error_signo');
    const errorEtnia = document.querySelector('#error_etnia');
    const errorCorCabelo = document.querySelector('#error_cor_cabelo');
    const errorCorOlhos = document.querySelector('#error_cor_olhos');
    const errorAltura = document.querySelector('#error_altura');
    const errorBebe = document.querySelector('#error_bebe');
    const errorTipoCorpo = document.querySelector('#error_tipo_corpo');
    const errorFuma = document.querySelector('#error_fuma');
    const errorDescricao = document.querySelector('#error_descricao');
    const errorForm = document.querySelector('#error_form');

    const loader = document.querySelector('.loader');
    const botaoEnviar = document.querySelector('#enviar');

    /* const requestPOST = document.querySelector('#request-post');

    function botaDadosRequestPost(){
        let dadosRequestPOST = requestPOST.getAttribute('request_post');
        dadosRequestPOST = dadosRequestPOST.replace('<QueryDict: ', '').replace('>', '').replace(/'/g, '"');
        dadosRequestPOST = JSON.parse(dadosRequestPOST);
        
        if(dadosRequestPOST.nome){nome.value = dadosRequestPOST.nome;}
        if(dadosRequestPOST.genero){genero.value = dadosRequestPOST.genero;}
        if(dadosRequestPOST.data){data.value = dadosRequestPOST.data;}
        if(dadosRequestPOST.nacionalidade){nacionalidade.value = dadosRequestPOST.nacionalidade;}
        if(dadosRequestPOST.email){email.value = dadosRequestPOST.email;}
        if(dadosRequestPOST.pais){pais.value = dadosRequestPOST.pais;}
        if(dadosRequestPOST.interesses){interesses.value = dadosRequestPOST.interesses;}
        if(dadosRequestPOST.orientacaoSexual){orientacaoSexual.value = dadosRequestPOST.orientacaoSexual;}
        if(dadosRequestPOST.regiao){regiao.value = dadosRequestPOST.regiao;}
        if(dadosRequestPOST.estadoCivil){estadoCivil.value = dadosRequestPOST.estadoCivil;}
        if(dadosRequestPOST.signo){signo.value = dadosRequestPOST.signo;}
        if(dadosRequestPOST.etnia){etnia.value = dadosRequestPOST.etnia;}
        if(dadosRequestPOST.corCabelo){corCabelo.value = dadosRequestPOST.corCabelo;}
        if(dadosRequestPOST.corOlhos){corOlhos.value = dadosRequestPOST.corOlhos;}
        if(dadosRequestPOST.altura){altura.value = dadosRequestPOST.altura;}
        if(dadosRequestPOST.bebe){bebe.value = dadosRequestPOST.bebe;}
        if(dadosRequestPOST.tipoCorpo){tipoCorpo.value = dadosRequestPOST.tipoCorpo;}
        if(dadosRequestPOST.fuma){fuma.value = dadosRequestPOST.fuma;}
        if(dadosRequestPOST.descricao){descricao.value = dadosRequestPOST.descricao;}
    }
    botaDadosRequestPost(); */
    
    
    document.addEventListener('click', e => {

        const el = e.target;
        
    });

    document.addEventListener('input', e => {

        const el = e.target;

        if(el == descricao){
            if(descricao.value.length <= 10000){
                pDescricao.innerHTML = `Descrição: ${descricao.value.length}/10000 caracteres escritos`
            }
        }

        /* errorNome.innerHTML = '';
        errorUsuario.innerHTML = '';
        errorGenero.innerHTML = '';
        errorData.innerHTML = '';
        errorNacionalidade.innerHTML = '';
        errorEmail.innerHTML = '';
        errorPais.innerHTML = '';
        errorCelular.innerHTML = '';
        errorRegiao.innerHTML = '';
        errorInteresses.innerHTML = '';
        errorOrientacaoSexual.innerHTML = '';
        errorProfissao.innerHTML = '';
        errorEstadoCivil.innerHTML = '';
        errorSigno.innerHTML = '';
        errorEtnia.innerHTML = '';
        errorCorCabelo.innerHTML = '';
        errorCorOlhos.innerHTML = '';
        errorAltura.innerHTML = '';
        errorBebe.innerHTML = '';
        errorTipoCorpo.innerHTML = '';
        errorFuma.innerHTML = '';
        errorDescricao.innerHTML = '';
        errorForm.innerHTML = ''; */

        // Checkbox Logic
        // Nome
        if(el == checkboxNome && checkboxNome.checked){
            nome.classList.add('selecionado');
        } else if(el == checkboxNome && !checkboxNome.checked){
            nome.classList.remove('selecionado');
        }

        // Gênero
        if(el == checkboxGenero && checkboxGenero.checked){
            genero.classList.add('selecionado');
        } else if(el == checkboxGenero && !checkboxGenero.checked){
            genero.classList.remove('selecionado');
        }

        // Data
        if(el == checkboxData && checkboxData.checked){
            data.classList.add('selecionado');
        } else if(el == checkboxData && !checkboxData.checked){
            data.classList.remove('selecionado');
        }

        // Nacionalidade
        if(el == checkboxNacionalidade && checkboxNacionalidade.checked){
            nacionalidade.classList.add('selecionado');
        } else if(el == checkboxNacionalidade && !checkboxNacionalidade.checked){
            nacionalidade.classList.remove('selecionado');
        }

        // E-mail
        if(el == checkboxEmail && checkboxEmail.checked){
            email.classList.add('selecionado');
        } else if(el == checkboxEmail && !checkboxEmail.checked){
            email.classList.remove('selecionado');
        }

        // Pais
        if(el == checkboxPais && checkboxPais.checked){
            pais.classList.add('selecionado');
        } else if(el == checkboxPais && !checkboxPais.checked){
            pais.classList.remove('selecionado');
        }

        // Celular
        if(el == checkboxCelular && checkboxCelular.checked){
            celular.classList.add('selecionado');
        } else if(el == checkboxCelular && !checkboxCelular.checked){
            celular.classList.remove('selecionado');
        }

        // Profissão
        if(el == checkboxProfissao && checkboxProfissao.checked){
            profissao.classList.add('selecionado');
        } else if(el == checkboxProfissao && !checkboxProfissao.checked){
            profissao.classList.remove('selecionado');
        }

        // Regiao
        if(el == checkboxRegiao && checkboxRegiao.checked){
            regiao.classList.add('selecionado');
        } else if(el == checkboxRegiao && !checkboxRegiao.checked){
            regiao.classList.remove('selecionado');
        }

        // Interesses
        if(el == checkboxInteresses && checkboxInteresses.checked){
            interesses.classList.add('selecionado');
        } else if(el == checkboxInteresses && !checkboxInteresses.checked){
            interesses.classList.remove('selecionado');
        }

        // Orientação sexual
        if(el == checkboxOrientacaoSexual && checkboxOrientacaoSexual.checked){
            orientacaoSexual.classList.add('selecionado');
        } else if(el == checkboxOrientacaoSexual && !checkboxOrientacaoSexual.checked){
            orientacaoSexual.classList.remove('selecionado');
        }

        // Estado civil
        if(el == checkboxEstadoCivil && checkboxEstadoCivil.checked){
            estadoCivil.classList.add('selecionado');
        } else if(el == checkboxEstadoCivil && !checkboxEstadoCivil.checked){
            estadoCivil.classList.remove('selecionado');
        }

        // Signo
        if(el == checkboxSigno && checkboxSigno.checked){
            signo.classList.add('selecionado');
        } else if(el == checkboxSigno && !checkboxSigno.checked){
            signo.classList.remove('selecionado');
        }

        // Etnia
        if(el == checkboxEtnia && checkboxEtnia.checked){
            etnia.classList.add('selecionado');
        } else if(el == checkboxEtnia && !checkboxEtnia.checked){
            etnia.classList.remove('selecionado');
        }

        // Cor do cabelo
        if(el == checkboxCorCabelo && checkboxCorCabelo.checked){
            corCabelo.classList.add('selecionado');
        } else if(el == checkboxCorCabelo && !checkboxCorCabelo.checked){
            corCabelo.classList.remove('selecionado');
        }

        // Cor dos olhos
        if(el == checkboxCorOlhos && checkboxCorOlhos.checked){
            corOlhos.classList.add('selecionado');
        } else if(el == checkboxCorOlhos && !checkboxCorOlhos.checked){
            corOlhos.classList.remove('selecionado');
        }

        // Altura
        if(el == checkboxAltura && checkboxAltura.checked){
            altura.classList.add('selecionado');
        } else if(el == checkboxAltura && !checkboxAltura.checked){
            altura.classList.remove('selecionado');
        }

        // Tipo corpo
        if(el == checkboxTipoCorpo && checkboxTipoCorpo.checked){
            tipoCorpo.classList.add('selecionado');
        } else if(el == checkboxTipoCorpo && !checkboxTipoCorpo.checked){
            tipoCorpo.classList.remove('selecionado');
        }

        // Fuma
        if(el == checkboxFuma && checkboxFuma.checked){
            fuma.classList.add('selecionado');
        } else if(el == checkboxFuma && !checkboxFuma.checked){
            fuma.classList.remove('selecionado');
        }

        // Bebe
        if(el == checkboxBebe && checkboxBebe.checked){
            bebe.classList.add('selecionado');
        } else if(el == checkboxBebe && !checkboxBebe.checked){
            bebe.classList.remove('selecionado');
        }

        // Descrição
        if(el == checkboxDescricao && checkboxDescricao.checked){
            descricao.classList.add('selecionado');
            pDescricao.style.display = 'inline-block';
        } else if(el == checkboxDescricao && !checkboxDescricao.checked){
            descricao.classList.remove('selecionado');
            pDescricao.style.display = 'none';
        }

        // Foto
        if(el == checkboxFoto && checkboxFoto.checked){
            foto.classList.add('selecionado');
        } else if(el == checkboxFoto && !checkboxFoto.checked){
            foto.classList.remove('selecionado');
        }

    });

    document.addEventListener('submit', e => {
        validador = true;

        errorNome.innerHTML = '';
        errorGenero.innerHTML = '';
        errorData.innerHTML = '';
        errorNacionalidade.innerHTML = '';
        errorEmail.innerHTML = '';
        errorPais.innerHTML = '';
        errorCelular.innerHTML = '';
        errorRegiao.innerHTML = '';
        errorInteresses.innerHTML = '';
        errorOrientacaoSexual.innerHTML = '';
        errorProfissao.innerHTML = '';
        errorEstadoCivil.innerHTML = '';
        errorSigno.innerHTML = '';
        errorEtnia.innerHTML = '';
        errorCorCabelo.innerHTML = '';
        errorCorOlhos.innerHTML = '';
        errorAltura.innerHTML = '';
        errorBebe.innerHTML = '';
        errorTipoCorpo.innerHTML = '';
        errorFuma.innerHTML = '';
        errorDescricao.innerHTML = '';
        errorForm.innerHTML = '';
        
        if(checkboxNome.checked && !nome.value){
            validador = false;
            errorNome.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxGenero.checked && genero.value == 'Gênero'){
            validador = false;
            errorGenero.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        // Validando data e  vendo se é menor que 18 anos - Início
        if(checkboxData.checked && !data.value){
            validador = false;
            errorData.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        } else if(checkboxData.checked){
            const regexData = /^\d{2}\/\d{2}\/\d{4}$/;

            if (!regexData.test(data.value)) {
                e.preventDefault();
                validador = false;
                errorData.innerHTML = 'Formato de data inválido. Use o formato 00/00/0000.';
            } else{
                const [dia, mes, ano] = data.value.split('/').map(Number);
                
                if (parseInt(mes) <= 0 || parseInt(mes) > 12 || parseInt(dia) <= 0 || parseInt(dia) > 31){
                    validador = false;
                    errorData.innerHTML = 'Data inválida.';
                } else{
                    const dataAniversario = new Date(ano, parseInt(mes) - 1, dia);

                    // Verificação de validade da data
                    if (dataAniversario.getDate() != dia || dataAniversario.getMonth() + 1 != mes || dataAniversario.getFullYear() != ano) {
                        validador = false;
                        errorData.innerHTML = 'Essa data não existe.';""
                    } else{
                        const diaAniversario = dataAniversario.getUTCDate();
                        const mesAniversario = dataAniversario.getUTCMonth() + 1;
                        const anoAniversario = dataAniversario.getUTCFullYear();

                        const diaAtual = new Date().getUTCDate();
                        const mesAtual = new Date().getUTCMonth() + 1;
                        const anoAtual = new Date().getUTCFullYear();

                        let idade = anoAtual - anoAniversario;
                        if (mesAtual < mesAniversario || (mesAtual === mesAniversario && diaAtual < diaAniversario)) {
                            idade--;
                        }

                        if(idade < 18){
                            e.preventDefault();
                            validador = false;
                            errorData.innerHTML = 'Você tem que ter mais de 18 anos para usar o site.';
                        }
                    }
                }
            }
        }
        // Validando data e  vendo se é maior que 18 anos - Fim

        if(checkboxNacionalidade.checked && !nacionalidade.value){
            validador = false;
            errorNacionalidade.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxEmail.checked && !email.value){
            validador = false;
            errorEmail.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxPais.checked && pais.value == 'País'){
            validador = false;
            errorPais.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxCelular.checked && !celular.value){
            validador = false;
            errorCelular.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxRegiao.checked && !regiao.value){
            validador = false;
            errorRegiao.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxInteresses.checked && interesses.value == 'Interesses'){
            validador = false;
            errorInteresses.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxOrientacaoSexual.checked && orientacaoSexual.value == 'Orientação Sexual'){
            validador = false;
            errorOrientacaoSexual.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxProfissao.checked && !profissao.value){
            validador = false;
            errorProfissao.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxEstadoCivil.checked && estadoCivil.value == 'Estado Civil'){
            validador = false;
            errorEstadoCivil.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxSigno.checked && signo.value == 'Signo'){
            validador = false;
            errorSigno.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxEtnia.checked && etnia.value == 'Etnia'){
            validador = false;
            errorEtnia.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxCorCabelo.checked && corCabelo.value == 'Cor do Cabelo'){
            validador = false;
            errorCorCabelo.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxCorOlhos.checked && corOlhos.value == 'Cor dos Olhos'){
            validador = false;
            errorCorOlhos.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxTipoCorpo.checked && tipoCorpo.value == 'Tipo de Corpo'){
            validador = false;
            errorTipoCorpo.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxAltura.checked && altura.value == 'Altura'){
            validador = false;
            errorAltura.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxFuma.checked && fuma.value == 'Fuma?'){
            validador = false;
            errorFuma.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxBebe.checked && bebe.value == 'Bebe?'){
            validador = false;
            errorBebe.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(checkboxDescricao.checked && !descricao.value){
            validador = false;
            errorDescricao.innerHTML = 'Se você selecionou o campo acima, ele NÃO pode ficar vazio.';
        }

        if(validador){
            loader.style.display = 'inline-block';
            botaoEnviar.style.display = 'none';
        } else{
            e.preventDefault();
            errorForm.innerHTML = 'Erro no formulário';
        }
    });

})();
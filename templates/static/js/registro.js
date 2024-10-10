(function(){

    const primeiraParte = document.querySelector('.primeira_parte');
    const segundaParte = document.querySelector('.segunda_parte');

    const nome = document.querySelector('#nome');
    const genero = document.querySelector('#genero');
    const errorNomeGenero = document.querySelector('#error_nome_genero');

    //const usuario = document.querySelector('#usuario');
    //const errorUsuario = document.querySelector('#error_usuario');

    const data = document.querySelector('#data');
    const errorData = document.querySelector('#error_data');

    const nacionalidade = document.querySelector('#nacionalidade');
    const email = document.querySelector('#email');
    const errorNacionalidadeEmail = document.querySelector('#error_nacionalidade_email');

    const senha1 = document.querySelector('#senha1');
    const senha2 = document.querySelector('#senha2');
    const errorSenhas = document.querySelector('#error_senhas');

    const pais = document.querySelector('#pais');
    const celular = document.querySelector('#celular');
    const errorPaisCelular = document.querySelector('#error_pais_celular');

    const regiao = document.querySelector('#regiao');
    const errorRegiao = document.querySelector('#error_regiao');

    const interesses = document.querySelector('#interesses');
    const errorInteresses = document.querySelector('#error_interesses');

    const orientacaoSexual = document.querySelector('#orientacao_sexual');
    const profissao = document.querySelector('#profissao');
    const errorOrientacaoSexualProfissao = document.querySelector('#error_orientacao_sexual_profissao');

    const estadoCivil = document.querySelector('#estado_civil');
    const signo = document.querySelector('#signo');
    const errorEstadoCivilSigno = document.querySelector('#error_estado_civil_signo');

    const etnia = document.querySelector('#etnia');
    const corCabelo = document.querySelector('#cor_cabelo');
    const errorEtniaCorCabelo = document.querySelector('#error_etnia_cor_cabelo');

    const corOlhos = document.querySelector('#cor_olhos');
    const altura = document.querySelector('#altura');
    const errorCorOlhosAltura = document.querySelector('#error_cor_olhos_altura');

    const bebe = document.querySelector('#bebe');
    const errorBeber = document.querySelector('#error_beber');

    const tipoCorpo = document.querySelector('#tipo_corpo');
    const fuma = document.querySelector('#fuma');
    const errorTipoCorpoFuma = document.querySelector('#error_tipo_corpo_fuma');

    const descricao = document.querySelector('#descricao');
    const pDescricao = document.querySelector('.p-descricao');
    const errorDescricao = document.querySelector('#error_descricao');

    const aceitarTermos = document.querySelector('#aceitar-termos');
    const errorAceitarTermos = document.querySelector('#error_aceitar_termos');

    const fotoInput = document.querySelector('#foto-perfil');
    const errorFoto = document.querySelector('#error_foto_perfil');

    const errorGeral = document.querySelector('#error_geral');

    const botaoVoltar = document.querySelector('.voltar');

    const loader = document.querySelector('.loader');
    const botaoEnviar = document.querySelector('#enviar');

    const form = document.querySelector('#form');

    const requestPOST = document.querySelector('#request-post');
    
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
        if(dadosRequestPOST.orientacao_sexual){orientacaoSexual.value = dadosRequestPOST.orientacao_sexual;}
        if(dadosRequestPOST.profissao){profissao.value = dadosRequestPOST.profissao;}
        if(dadosRequestPOST.regiao){regiao.value = dadosRequestPOST.regiao;}
        if(dadosRequestPOST.estado_civil){estadoCivil.value = dadosRequestPOST.estado_civil;}
        if(dadosRequestPOST.signo){signo.value = dadosRequestPOST.signo;}
        if(dadosRequestPOST.etnia){etnia.value = dadosRequestPOST.etnia;}
        if(dadosRequestPOST.cor_cabelo){corCabelo.value = dadosRequestPOST.cor_cabelo;}
        if(dadosRequestPOST.cor_olhos){corOlhos.value = dadosRequestPOST.cor_olhos;}
        if(dadosRequestPOST.altura){altura.value = dadosRequestPOST.altura;}
        if(dadosRequestPOST.bebe){bebe.value = dadosRequestPOST.bebe;}
        if(dadosRequestPOST.tipo_corpo){tipoCorpo.value = dadosRequestPOST.tipo_corpo;}
        if(dadosRequestPOST.fuma){fuma.value = dadosRequestPOST.fuma;}
        if(dadosRequestPOST.descricao){descricao.value = dadosRequestPOST.descricao;}
    }
    botaDadosRequestPost();
    
    document.addEventListener('click', e => {

        const el = e.target;

        if(el == botaoVoltar){
            e.preventDefault();
            primeiraParte.style.display = 'flex';
            segundaParte.style.display = 'none';
        }

    });

    document.addEventListener('input', e => {

        const el = e.target;

        if(el == descricao){
            if(descricao.value.length <= 10000){
                pDescricao.innerHTML = `Descrição: ${descricao.value.length}/10000 caracteres escritos`
            }
        }

    });

    document.addEventListener('submit', e => {

        errorNomeGenero.innerHTML = '';
        errorNomeGenero.style.display = 'none';

        //errorUsuario.innerHTML = '';
        //errorUsuario.style.display = 'none';

        errorData.innerHTML = '';
        errorData.style.display = 'none';

        errorNacionalidadeEmail.innerHTML = '';
        errorNacionalidadeEmail.style.display = 'none';

        errorSenhas.innerHTML = '';
        errorSenhas.style.display = 'none';

        errorPaisCelular.innerHTML = '';
        errorPaisCelular.style.display = 'none';

        errorRegiao.innerHTML = '';
        errorRegiao.style.display = 'none';

        errorInteresses.innerHTML = '';
        errorInteresses.style.display = 'none';

        errorOrientacaoSexualProfissao.innerHTML = '';
        errorOrientacaoSexualProfissao.style.display = 'none';

        errorEstadoCivilSigno.innerHTML = '';
        errorEstadoCivilSigno.style.display = 'none';

        errorEtniaCorCabelo.innerHTML = '';
        errorEtniaCorCabelo.style.display = 'none';

        errorCorOlhosAltura.innerHTML = '';
        errorCorOlhosAltura.style.display = 'none';

        errorBeber.innerHTML = '';
        errorBeber.style.display = 'none';

        errorTipoCorpoFuma.innerHTML = '';
        errorTipoCorpoFuma.style.display = 'none';

        errorDescricao.innerHTML = '';
        errorDescricao.style.display = 'none';

        errorFoto.innerHTML = '';
        errorFoto.style.display = 'none';

        errorAceitarTermos.innerHTML = '';
        errorAceitarTermos.style.display = 'none';

        aceitarTermos.innerHTML = '';
        errorAceitarTermos.style.display = 'none';

        let validadorPrimeiraEtapa = true;
        let validadorTudo = true;

        if(!nome.value && genero.value == 'Gênero'){
            e.preventDefault();
            errorNomeGenero.style.display = 'inline-block';
            errorNomeGenero.innerHTML = 'Os campos de "nome" e "gênero" não podem ficar vazios.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(!nome.value){
            e.preventDefault();
            errorNomeGenero.style.display = 'inline-block';
            errorNomeGenero.innerHTML = 'O campo de "nome" não pode ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(genero.value == 'Gênero'){
            e.preventDefault();
            errorNomeGenero.style.display = 'inline-block';
            errorNomeGenero.innerHTML = 'O campo "gênero" não podem ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        }

        /* if(!usuario.value){
            e.preventDefault();
            errorUsuario.style.display = 'inline-block';
            errorUsuario.innerHTML = 'O campo de "usuário" não pode ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(usuario.value.length < 4){
            e.preventDefault();
            errorUsuario.style.display = 'inline-block';
            errorUsuario.innerHTML = 'O usuário tem que ter no mínimo 4 caracteres.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } */

        // Validando data e  vendo se é menor que 18 anos - Início
        if(!data.value){
            e.preventDefault();
            errorData.style.display = 'inline-block';
            errorData.innerHTML = 'O campo "data" não pode ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else{
            const regexData = /^\d{2}\/\d{2}\/\d{4}$/;

            if (!regexData.test(data.value)) {
                e.preventDefault();
                errorData.style.display = 'inline-block';
                errorData.innerHTML = 'Formato de data inválido. Use o formato 00/00/0000.';
                validadorPrimeiraEtapa = false;
                validadorTudo = false;
            } else{
                const [dia, mes, ano] = data.value.split('/').map(Number);
                
                if (parseInt(mes) <= 0 || parseInt(mes) > 12 || parseInt(dia) <= 0 || parseInt(dia) > 31){
                    e.preventDefault();
                    errorData.style.display = 'inline-block';
                    errorData.innerHTML = 'Data inválida.';
                    validadorPrimeiraEtapa = false;
                    validadorTudo = false;
                } else{
                    const dataAniversario = new Date(ano, parseInt(mes) - 1, dia);

                    // Verificação de validade da data
                    if (dataAniversario.getDate() != dia || dataAniversario.getMonth() + 1 != mes || dataAniversario.getFullYear() != ano) {
                        e.preventDefault();
                        errorData.style.display = 'inline-block';
                        errorData.innerHTML = 'Essa data não existe.';
                        validadorPrimeiraEtapa = false;
                        validadorTudo = false;
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
                            errorData.style.display = 'inline-block';
                            errorData.innerHTML = 'Você tem que ter mais de 18 anos para usar o site.';
                            validadorPrimeiraEtapa = false;
                            validadorTudo = false;
                        }
                    }
                }
            }
        }
        // Validando data e  vendo se é menor que 18 anos - Fim

        if(!nacionalidade.value && !email.value){
            e.preventDefault();
            errorNacionalidadeEmail.style.display = 'inline-block';
            errorNacionalidadeEmail.innerHTML = 'Os campos de "nacionalidade" e "e-mail" não podem ficar vazios.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(!nacionalidade.value){
            e.preventDefault();
            errorNacionalidadeEmail.style.display = 'inline-block';
            errorNacionalidadeEmail.innerHTML = 'O campo de "nacionalidade" não pode ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(!email.value){
            e.preventDefault();
            errorNacionalidadeEmail.style.display = 'inline-block';
            errorNacionalidadeEmail.innerHTML = 'O campo "e-mail" não podem ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        }


        if(!senha1.value && !senha2.value){
            e.preventDefault();
            errorSenhas.style.display = 'inline-block';
            errorSenhas.innerHTML = 'Os campos de "senha" e "repetir senha" não podem ficar vazios.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(!senha1.value || !senha2.value){
            e.preventDefault();
            errorSenhas.style.display = 'inline-block';
            errorSenhas.innerHTML = 'Os campos de "senha" e "repetir senha" não podem ficar vazios.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(senha1.value != senha2.value){
            e.preventDefault();
            errorSenhas.style.display = 'inline-block';
            errorSenhas.innerHTML = 'O campo de "senha" e "repetir senha" tem que ser iguais.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(senha2.value.length < 5){
            e.preventDefault();
            errorSenhas.style.display = 'inline-block';
            errorSenhas.innerHTML = 'O campo de "senha" e "repetir senha" precisam ter no mínimo de 5 caracteres.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        }


        if(pais.value == 'Selecione o país' && !celular.value){
            e.preventDefault();
            errorPaisCelular.style.display = 'inline-block';
            errorPaisCelular.innerHTML = 'Os campos de "pais" e "celular" não podem ficar vazios.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(pais.value == 'Selecione o país'){
            e.preventDefault();
            errorPaisCelular.style.display = 'inline-block';
            errorPaisCelular.innerHTML = 'O campo de "pais" não pode ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        } else if(!celular.value){
            e.preventDefault();
            errorPaisCelular.style.display = 'inline-block';
            errorPaisCelular.innerHTML = 'O campo de "celular" não pode ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        }

        if(!regiao.value){
            e.preventDefault();
            errorRegiao.style.display = 'inline-block';
            errorRegiao.innerHTML = 'O campo de "região" não pode ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        }

        if(interesses.value == 'Interesses'){
            e.preventDefault();
            errorInteresses.style.display = 'inline-block';
            errorInteresses.innerHTML = 'O campo de "interesse" não pode ficar vazio.';
            validadorPrimeiraEtapa = false;
            validadorTudo = false;
        }

        let val = false;
        if(segundaParte.getAttribute('style') == 'display: flex;'){
            val = true;
        }

        if(validadorPrimeiraEtapa){
            e.preventDefault();
            primeiraParte.style.display = 'none';
            segundaParte.style.display = 'flex';
        }

        if(val){
            if(orientacaoSexual.value == 'Orientação Sexual' && !profissao.value){
                e.preventDefault();
                errorOrientacaoSexualProfissao.style.display = 'inline-block';
                errorOrientacaoSexualProfissao.innerHTML = 'Os campos de "orientação sexual" e "profissão" não podem ficar vazios.';
                validadorTudo = false;
            } else if(orientacaoSexual.value == 'Orientação Sexual'){
                e.preventDefault();
                errorOrientacaoSexualProfissao.style.display = 'inline-block';
                errorOrientacaoSexualProfissao.innerHTML = 'O campo de "orientação sexual" não pode ficar vazio.';
                validadorTudo = false;
            } else if(!profissao.value){
                e.preventDefault();
                errorOrientacaoSexualProfissao.style.display = 'inline-block';
                errorOrientacaoSexualProfissao.innerHTML = 'O campo "profissão" não pode ficar vazio.';
                validadorTudo = false;
            }
    
            if(estadoCivil.value == 'Estado Civil' && signo.value == 'Signo'){
                e.preventDefault();
                errorEstadoCivilSigno.style.display = 'inline-block';
                errorEstadoCivilSigno.innerHTML = 'Os campos de "estado civil" e "signo" não podem ficar vazios.';
                validadorTudo = false;
            } else if(estadoCivil.value == 'Estado Civil'){
                e.preventDefault();
                errorEstadoCivilSigno.style.display = 'inline-block';
                errorEstadoCivilSigno.innerHTML = 'O campo de "estado civil" não pode ficar vazio.';
                validadorTudo = false;
            } else if(signo.value == 'Signo'){
                e.preventDefault();
                errorEstadoCivilSigno.style.display = 'inline-block';
                errorEstadoCivilSigno.innerHTML = 'O campo "signo" não pode ficar vazio.';
                validadorTudo = false;
            }
    
            if(etnia.value == 'Etnia' && corCabelo.value == 'Cor do Cabelo'){
                e.preventDefault();
                errorEtniaCorCabelo.style.display = 'inline-block';
                errorEtniaCorCabelo.innerHTML = 'Os campos de "etnia" e "cor do cabelo" não podem ficar vazios.';
                validadorTudo = false;
            } else if(etnia.value == 'Etnia'){
                e.preventDefault();
                errorEtniaCorCabelo.style.display = 'inline-block';
                errorEtniaCorCabelo.innerHTML = 'O campo de "etnia" não pode ficar vazio.';
                validadorTudo = false;
            } else if(corCabelo.value == 'Cor do Cabelo'){
                e.preventDefault();
                errorEtniaCorCabelo.style.display = 'inline-block';
                errorEtniaCorCabelo.innerHTML = 'O campo "cor do cabelo" não pode ficar vazio.';
                validadorTudo = false;
            }
    
            if(corOlhos.value == 'Cor dos Olhos' && altura.value == 'Altura'){
                e.preventDefault();
                errorCorOlhosAltura.style.display = 'inline-block';
                errorCorOlhosAltura.innerHTML = 'Os campos de "cor dos olhos" e "altura" não podem ficar vazios.';
                validadorTudo = false;
            } else if(corOlhos.value == 'Cor dos Olhos'){
                e.preventDefault();
                errorCorOlhosAltura.style.display = 'inline-block';
                errorCorOlhosAltura.innerHTML = 'O campo de "cor dos olhos" não pode ficar vazio.';
                validadorTudo = false;
            } else if(altura.value == 'Altura'){
                e.preventDefault();
                errorCorOlhosAltura.style.display = 'inline-block';
                errorCorOlhosAltura.innerHTML = 'O campo "altura" não pode ficar vazio.';
                validadorTudo = false;
            }
    
            if(tipoCorpo.value == 'Tipo de Corpo' && fuma.value == 'Fuma?'){
                e.preventDefault();
                errorTipoCorpoFuma.style.display = 'inline-block';
                errorTipoCorpoFuma.innerHTML = 'Os campos de "tipo de corpo" e "fumar" não podem ficar vazios.';
                validadorTudo = false;
            } else if(tipoCorpo.value == 'Tipo de Corpo'){
                e.preventDefault();
                errorTipoCorpoFuma.style.display = 'inline-block';
                errorTipoCorpoFuma.innerHTML = 'O campo de "tipo de corpo" não pode ficar vazio.';
                validadorTudo = false;
            } else if(fuma.value == 'Fuma?'){
                e.preventDefault();
                errorTipoCorpoFuma.style.display = 'inline-block';
                errorTipoCorpoFuma.innerHTML = 'O campo "fumar" não pode ficar vazio.';
                validadorTudo = false;
            }
    
            if(bebe.value == 'Bebe?'){
                e.preventDefault();
                errorBeber.style.display = 'inline-block';
                errorBeber.innerHTML = 'O campo de "beber" não pode ficar vazio.';
                validadorTudo = false;
            }
    
            if(!descricao.value){
                e.preventDefault();
                errorDescricao.style.display = 'inline-block';
                errorDescricao.innerHTML = 'O campo de "descrição" não pode ficar vazio.';
                validadorTudo = false;
            }

            if(!fotoInput.value){
                e.preventDefault();
                errorFoto.style.display = 'inline-block';
                errorFoto.innerHTML = 'Enviar uma foto de perfil é obrigatório';
                validadorTudo = false;
            }
            
            if(!aceitarTermos.checked){
                e.preventDefault();
                errorAceitarTermos.style.display = 'inline-block';
                errorAceitarTermos.innerHTML = 'Para realizar o cadastro, você precisa aceitar política de privacidade e os termos de condições.';
                validadorTudo = false;
            }
    
            if(!validadorTudo){
                e.preventDefault();
                errorGeral.style.display = 'inline-block';
                errorGeral.innerHTML = 'Erro no formulário. Revise.';
            } else{
                loader.style.display = 'inline-block';
                botaoEnviar.style.display = 'none';
                form.submit();
            }

        }
        

    });

})();

// Todo o código agora está dentro deste evento, garantindo que o HTML foi carregado.
document.addEventListener('DOMContentLoaded', function() {
    
    // =======================================================
    // 1. LÓGICA PARA MOSTRAR/ESCONDER DADOS DO RESPONSÁVEL
    // =======================================================
    const checkboxMenorIdade = document.getElementById('menorIdade');
    const secaoResponsavel = document.getElementById('secao-responsavel');

    if (checkboxMenorIdade && secaoResponsavel) {
        
        function toggleResponsavel() {
            const camposResponsavel = secaoResponsavel.querySelectorAll('input, select');

            if (checkboxMenorIdade.checked) {
                secaoResponsavel.style.display = 'grid';
                camposResponsavel.forEach(campo => campo.required = true);
            } else {
                secaoResponsavel.style.display = 'none';
                camposResponsavel.forEach(campo => {
                    campo.required = false;
                    campo.value = '';
                });
            }
        }

        checkboxMenorIdade.addEventListener('change', toggleResponsavel);
        toggleResponsavel(); // Garante o estado inicial correto
    }

    // =======================================================
    // 2. MÁSCARAS E VALIDAÇÕES DOS CAMPOS (INPUTS)
    // =======================================================
    function limparApenasLetras(input) {
        input.value = input.value.replace(/[^A-Za-zÀ-ÿ\s]/g, '');
    }

    function limparApenasNumeros(input) {
        input.value = input.value.replace(/\D/g, '');
    }

    document.querySelectorAll('.apenas-letras').forEach(input => {
        input.addEventListener('input', () => limparApenasLetras(input));
    });

    document.querySelectorAll('.cpf').forEach(input => {
        input.setAttribute('maxlength', '11');
        input.addEventListener('input', () => limparApenasNumeros(input));
    });

    document.querySelectorAll('.telefone').forEach(input => {
        input.setAttribute('maxlength', '11');
        input.addEventListener('input', () => limparApenasNumeros(input));
    });

    // =======================================================
    // 3. VALIDAÇÃO GERAL ANTES DE ENVIAR O FORMULÁRIO
    // =======================================================
    document.querySelector('form').addEventListener('submit', function(e) {
        let formValido = true;

        // Itera sobre cada campo para validação individual
        document.querySelectorAll('.cpf[required]').forEach(input => {
            if (formValido && input.value.length !== 11) {
                alert('O CPF "' + (input.placeholder || 'do responsável') + '" deve conter exatamente 11 números.');
                input.focus();
                formValido = false;
            }
        });

        document.querySelectorAll('.telefone[required]').forEach(input => {
            if (formValido && (input.value.length < 10 || input.value.length > 11)) {
                alert('O Telefone "' + (input.placeholder || 'de urgência') + '" deve conter 10 ou 11 números (com DDD).');
                input.focus();
                formValido = false;
            }
        });
        
        // Se alguma validação falhou, previne o envio do formulário
        if (!formValido) {
            e.preventDefault();
        }
    });

});

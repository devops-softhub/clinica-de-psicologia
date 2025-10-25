document.addEventListener('DOMContentLoaded', function() {
    // CORREÇÃO 1: Usar o ID do seu HTML (inscricao-form)
    const form = document.getElementById('inscricao-form'); 
    
    // Se o formulário não for encontrado, para o script
    if (!form) {
        console.error("Erro Crítico: O formulário com ID 'inscricao-form' não foi encontrado.");
        return; 
    }

    const checkboxMenorIdade = document.getElementById('menorIdade');
    const secaoResponsavel = document.getElementById('secao-responsavel');
    // Pega o token CSRF de forma segura
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    // --- 1. Lógica para mostrar/ocultar dados do responsável (SUA LÓGICA - PRESERVADA) ---
    if (checkboxMenorIdade && secaoResponsavel) {
        function toggleResponsavel() {
            const camposResponsavel = secaoResponsavel.querySelectorAll('input, select');
            const isChecked = checkboxMenorIdade.checked; // Simplificado

            if (isChecked) {
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
        toggleResponsavel(); // Inicializa o estado correto ao carregar
    }

    // --- 2. NOVAS FUNÇÕES (Para exibir erros) ---

    /** Limpa todas as mensagens de erro e bordas vermelhas. */
    function clearErrors() {
        // Remove mensagens de erro
        form.querySelectorAll('.error-message').forEach(el => el.remove());
        
        // Remove bordas de erro
        form.querySelectorAll('.input-error').forEach(el => {
            el.classList.remove('input-error');
        });
    }

    /** Exibe os erros vindos do Django no formulário. */
    function displayErrors(erros) {
        console.log("Erros de validação do Django:", erros); // Mantém o log
        
        // Itera sobre cada campo que tem erro
        for (const [fieldName, errorMessages] of Object.entries(erros)) {
            // Tenta encontrar o campo pelo ID (que deve ser o mesmo que o fieldName do forms.py)
            const campo = document.getElementById(fieldName); 
            
            if (campo) {
                // Adiciona a borda vermelha
                campo.classList.add('input-error');
                
                // Cria e insere a mensagem de erro logo após o campo
                const erroEl = document.createElement('span');
                erroEl.className = 'error-message';
                erroEl.textContent = errorMessages.join(' '); // Junta múltiplas mensagens
                
                campo.parentNode.insertBefore(erroEl, campo.nextSibling);
            } else {
                console.warn(`Campo de erro '${fieldName}' não encontrado no DOM.`);
            }
        }
        
        // Opcional: Rola a tela até o primeiro erro encontrado
        const firstError = document.querySelector('.error-message');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }


    // --- 3. Submissão do formulário (SUA LÓGICA - PRESERVADA E ALINHADA) ---
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Evita o envio tradicional do formulário
        
        // ADIÇÃO: Limpa erros antigos antes de enviar
        clearErrors(); 

        // 3. Coleta os dados do formulário (SUA LÓGICA)
        const formData = new FormData(form);
        
        // CORREÇÃO 2: A lista DEVE bater com os IDs do HTML e os nomes do forms.py
        const camposMultiplos = [
            'motivos_acompanhamento', 'doencas_fisicas', 'disponibilidade_semana',
            'pcd_neurodivergente', 'tipo_terapias', 'medicamentos_usados'
        ];
        
        // Converte o FormData para um objeto manualmente (SUA LÓGICA)
        const dadosObjeto = {};
        for (const [key, value] of formData.entries()) {
            if (camposMultiplos.includes(key)) {
                // Se a chave ainda não existe, cria como uma lista
                if (!dadosObjeto[key]) {
                    dadosObjeto[key] = formData.getAll(key);
                }
            } else if (key !== 'csrfmiddlewaretoken') { // Ignora o token aqui
                dadosObjeto[key] = value;
            }
        }
        
        // 4. Converte checkboxes em booleanos (SUA LÓGICA)
        dadosObjeto.menorIdade = checkboxMenorIdade ? checkboxMenorIdade.checked : false;
        const checkboxLGPD = document.getElementById('deAcordo');
        if (checkboxLGPD) {
            dadosObjeto.deAcordo = checkboxLGPD.checked;
        }

        console.log("Dados a serem enviados:", dadosObjeto); // Para debug

        // 5. CSRF token (Lógica movida para o topo)

        try {
            // Lógica de fetch (SUA LÓGICA)
            const response = await fetch('/formulario/cadastro/comunidade/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Usa o token pego no início
                },
                body: JSON.stringify(dadosObjeto)
            });

            const resultado = await response.json();

            // Lógica de sucesso (SUA LÓGICA - PRESERVADA)
            if (response.ok) {
                alert(resultado.mensagem || 'Inscrição realizada com sucesso!');
                form.reset();
                if (checkboxMenorIdade) { // Verifica se a var existe antes de chamar
                    toggleResponsavel(); // Garante que os campos sejam ocultados novamente
                }
            } 
            // CORREÇÃO 3: Substitui o 'alert' pela chamada da função 'displayErrors'
            else if (resultado.status === 'erro_validacao') {
                // alert('Por favor, corrija os erros no formulário.'); // REMOVIDO
                displayErrors(resultado.erros); // ADICIONADO
            } 
            // Lógica de erro do servidor (SUA LÓGICA - PRESERVADA)
            else {
                alert(`Erro do servidor: ${resultado.mensagem || 'Erro desconhecido.'}`);
            }

        } catch (error) {
            // Lógica de erro de comunicação (SUA LÓGICA - PRESERVADA)
            console.error('Erro de comunicação:', error);
            alert('Ocorreu um erro de comunicação com o servidor.');
        }
    });
});
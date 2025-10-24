document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-comunidade'); // Verifique se o ID do formulário é esse
    const checkboxMenorIdade = document.getElementById('menorIdade');
    const secaoResponsavel = document.getElementById('secao-responsavel');

    // --- 1. Lógica para mostrar/ocultar dados do responsável ---
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
        toggleResponsavel(); // Inicializa o estado correto ao carregar
    }

    // --- 2. Submissão do formulário ---
    if (form) {
        form.addEventListener('submit', async function(event) {
            event.preventDefault(); // Evita o envio tradicional do formulário

            // 3. Coleta os dados do formulário
            const formData = new FormData(form);
            const dadosObjeto = Object.fromEntries(formData.entries());

            // 4. Converte checkboxes em booleanos
            dadosObjeto.menorIdade = checkboxMenorIdade.checked;
            const checkboxLGPD = document.getElementById('deAcordo');
            if (checkboxLGPD) {
                dadosObjeto.deAcordo = checkboxLGPD.checked;
            }

            console.log("Dados a serem enviados:", dadosObjeto); // Para debug

            // 5. CSRF token
            const csrfToken = dadosObjeto.csrfmiddlewaretoken;
            delete dadosObjeto.csrfmiddlewaretoken; // Remova do corpo JSON

            try {
                const response = await fetch('/formulario/cadastro/comunidade', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify(dadosObjeto)
                });

                const resultado = await response.json();

                if (response.ok) {
                    alert(resultado.mensagem || 'Inscrição realizada com sucesso!');
                    form.reset();
                    toggleResponsavel(); // Garante que os campos sejam ocultados novamente
                } else if (resultado.status === 'erro_validacao') {
                    alert('Por favor, corrija os erros no formulário.');
                    console.log("Erros de validação do Django:", resultado.erros);
                    // Aqui você pode exibir os erros no HTML, se desejar
                } else {
                    alert(`Erro do servidor: ${resultado.mensagem || 'Erro desconhecido.'}`);
                }

            } catch (error) {
                console.error('Erro de comunicação:', error);
                alert('Ocorreu um erro de comunicação com o servidor.');
            }
        });
    }
});

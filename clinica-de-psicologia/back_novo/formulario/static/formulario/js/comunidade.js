// formulario/js/comunidade.js
document.addEventListener('DOMContentLoaded', function() {
    
    const checkboxMenorIdade = document.getElementById('menorIdade');
    const secaoResponsavel = document.getElementById('secao-responsavel');
    
    const form = document.getElementById('inscricao-form');

    if (form) {
        form.addEventListener('submit', async function(evento) {
            evento.preventDefault();
            
            let formValido = true;
            document.querySelectorAll('.cpf[required]').forEach(input => {
                if (formValido && input.value.length !== 11) {
                    alert('O CPF "' + (input.placeholder || 'do responsável') + '" deve conter exatamente 11 números.');
                    input.focus();
                    formValido = false;
                }
            });
            
            if (!formValido) {
                return;
            }

            // 3. Coleta os dados do formulário
            const formData = new FormData(form);
            const dadosObjeto = Object.fromEntries(formData.entries());
            dadosObjeto.menorIdade = document.getElementById('menorIdade').checked;
            dadosObjeto.deAcordo = document.getElementById('deAcordo').checked;

            console.log("Dados a serem enviados:", dadosObjeto); // Para depuração

            // 4. Pega o token CSRF
            const csrfToken = dadosObjeto.csrfmiddlewaretoken;

            // 5. Envia para o Django
            try {
                // ATENÇÃO: Verifique se a URL corresponde à do seu urls.py
                const response = await fetch('/api/inscricao/comunidade/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify(dadosObjeto)
                });

                const resultado = await response.json();

                if (response.ok) {
                    alert(resultado.mensagem);
                    form.reset();
                } else if (resultado.status === 'erro_validacao') {
                    alert('Por favor, corrija os erros no formulário.');
                    console.log("Erros de validação do Django:", resultado.erros);
                    // Aqui você pode adicionar lógica para mostrar os 'resultado.erros' no HTML
                } else {
                    alert(`Erro do servidor: ${resultado.mensagem}`);
                }

            } catch (error) {
                console.error('Erro de comunicação:', error);
                alert('Ocorreu um erro de comunicação com o servidor.');
            }
        });
    }
});
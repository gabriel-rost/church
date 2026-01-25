document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("webpush-subscribe-button");

    if (btn) {
        // Função que verifica e traduz
        const translateProcess = () => {
            const currentText = btn.innerText.toLowerCase();

            // Se achar 'subscribe' (mas não unsubscribe)
            if (currentText.includes("subscribe") && !currentText.includes("unsub")) {
                btn.innerHTML = '<i class="bi bi-bell-fill me-2"></i> Ativar Notificações';
            }
            // Se achar 'unsubscribe'
            else if (currentText.includes("unsubscribe")) {
                btn.innerHTML = '<i class="bi bi-bell-slash-fill me-2"></i> Desativar Notificações';
            }
        };

        // Tenta traduzir imediatamente
        translateProcess();

        // Tenta traduzir a cada 500ms durante os primeiros 3 segundos 
        // (para ganhar do carregamento lento do plugin)
        let attempts = 0;
        const interval = setInterval(() => {
            translateProcess();
            attempts++;
            if (attempts > 6) clearInterval(interval);
        }, 500);

        // Traduz também quando o usuário clica
        btn.addEventListener('click', () => {
            setTimeout(translateProcess, 1000);
        });
    }
});
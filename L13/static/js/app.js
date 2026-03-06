document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert[data-auto-dismiss="true"]');

    alerts.forEach((alertElement) => {
        window.setTimeout(() => {
            const alertInstance = bootstrap.Alert.getOrCreateInstance(alertElement);
            alertInstance.close();
        }, 4000);
    });
});

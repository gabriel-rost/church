self.addEventListener('push', function(event) {
    const data = event.data ? event.data.json() : {};

    event.waitUntil(
        self.registration.showNotification(
            data.head || 'Notificação',
            {
                body: data.body || '',
                icon: data.icon || '/static/img/icon.png',
                data: { url: data.url || '/' }
            }
        )
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});
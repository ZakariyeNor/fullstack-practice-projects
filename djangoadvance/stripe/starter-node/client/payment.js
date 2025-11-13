window.addEventListener('DOMContentLoaded', async () => {
    const { publishableKey } = await fetch('/config').then(r => r.json());
    const stripe = Stripe(publishableKey);

    const { clientSecret } = await fetch('/create-payment-intent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    }).then(r => r.json());

    const elements = stripe.elements({ clientSecret });
    const paymentElement = elements.create('payment');
    paymentElement.mount('#payment-element');

    const form = document.getElementById('payment-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const { error } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: window.location.href.split("?")[0] + "complete.html",
            },
        });

        if (error) {
            const messageContainer = document.querySelector('#error-messages');
            messageContainer.textContent = error.message;
        }
    });
});

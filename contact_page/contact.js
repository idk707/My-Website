function formatPhoneNumber(value) {
    value = value.replace(/\D/g, '');

    value = value.substring(0, 10);

    if (value.length > 3 && value.length <= 6) {
        value = value.slice(0,3) + '-' + value.slice(3);
    } else if (value.length > 6){
        value = value.slice(0,3) + '-' + value.slice(3,6) + '-' + value.slice(6);
    }
    return value;
}

document.getElementById('phoneNumber').addEventListener('input', function(e){
    const formatted = formatPhoneNumber(e.target.value);
    e.target.value = formatted;
});

const form = document.getElementById('contactForm');
const stats = document.getElementById('status');

form.addEventListener('submit', async function(e) {
    e.preventDefault();

    stats.innerText = "Sending...";

    const formData = new FormData(form);

    try{
        const response = await fetch('/send-message', {
            method: 'POST',
            body: formData
        });

        if(response.ok){
            stats.innerText = "Message sent successfully!";
            form.reset();
        } else {
            stats.innerText = "Failed to send message. Please try again.";
        }
    } catch (error) {
        console.error('Error:', error);
        stats.innerText = "An error occurred. Please try again.";
    }
});
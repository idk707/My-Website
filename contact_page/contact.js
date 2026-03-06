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

document.getElementById('contactForm').addEventListener('submit', function(e){
    e.preventDefault();

    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const phoneNumber = document.getElementById('phoneNumber').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

fetch("https://friendly-giggle-5ggj4jgg79q5hvq47-5501.app.github.dev/contact", {
    method: "POST",

    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        firstName,
        lastName,
        phoneNumber,
        email,
        message
    })
})
.then(res => res.json())
.then(data => {
    alert(data.message);
    this.reset();
})
.catch(err => console.error("Error:", err));
    });
        
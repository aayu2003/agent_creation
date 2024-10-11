function sendMessage() {
    const message = document.getElementById('message').value; // Get the message from the input field
    const userId = 'sedd'; // Your user ID
    const encodedMessage = encodeURIComponent(message); // Encode the message

    // Construct the API URL with the user_id and the encoded message
    const apiUrl = `https://aayu22102.pythonanywhere.com/chat/?user_id=sedd&message=%22where%20is%20IIIT%20Naya%20raipur%22`;

    // Log the message before sending
    console.log('Sending message:', apiUrl);

    // Send the message to the API
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }), // Sending the message as JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Message sent:', data);
        
        // Display the API response in the chat
        const messages = document.getElementById('messages'); // Get the messages list
        const li = document.createElement('li'); // Create a new list item
        li.textContent = data.response; // Assuming your API returns a 'response' field
        messages.appendChild(li); // Append the new list item to the messages list
        
        // Clear input after sending
        document.getElementById('message').value = ''; 
    })
    .catch(error => console.error('Error sending message:', error));
}
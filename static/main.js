let currentSession = null;

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        currentSession = data;
        document.getElementById('fileInfo').innerHTML = `
            File ready for transfer!<br>
            Session ID: ${data.session_id}
        `;
    } catch (error) {
        console.error('Upload error:', error);
    }
}

async function discoverDevices() {
    try {
        const response = await fetch('/discover');
        const devices = await response.json();
        
        const deviceList = document.getElementById('deviceList');
        deviceList.innerHTML = devices.map(device => `
            <li>${device.info} @ ${device.ip}</li>
        `).join('');
    } catch (error) {
        console.error('Discovery error:', error);
    }
}

async function initiateTransfer() {
    const sessionKey = document.getElementById('sessionKey').value;
    
    if (!currentSession || !sessionKey) {
        alert('Missing required information');
        return;
    }

    try {
        const response = await fetch(`/download/${currentSession.session_id}`, {
            headers: {
                'X-Encryption-Key': sessionKey
            }
        });
        
        if (response.ok) {
            alert('Transfer initiated successfully!');
        } else {
            alert('Transfer failed: ' + (await response.text()));
        }
    } catch (error) {
        console.error('Transfer error:', error);
    }
}
const mapCommandTopic = new ROSLIB.Topic({
    ros: ros,
    name: '/map_command',
    messageType: 'std_msgs/String'
});

function sendMapName() {
    const mapNameInput = document.getElementById('mapName');
    const mapName = mapNameInput.value.trim();

    if (mapName) {
        const message = new ROSLIB.Message({
            data: mapName
        });

        mapCommandTopic.publish(message);
        alert(`Comando per creare mappa '${mapName}' inviato!`);
    } else {
        alert('Inserisci un nome valido per la mappa.');
    }
}
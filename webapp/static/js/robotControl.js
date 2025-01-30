const cmdVelTopic = new ROSLIB.Topic({
    ros: ros,
    name: '/robot_commands',
    messageType: 'slam_robot/slam_robot_control'
  });
  
  function moveRobot(direction) {
    console.log(`direzione: ${direction}`)
    const validDirections = ["forward", "left", "right", "stop"];
    if (!validDirections.includes(direction)) {
      console.error(`Direzione non valida: ${direction}`);
      return;
    }
    const backward = document.getElementById('backward').checked;
  
    const message = new ROSLIB.Message({
      direction: direction,
      backward: backward
    });
  
    cmdVelTopic.publish(message);
    console.log(`Comando inviato: ${direction}, ${backward}`);
  }
  
  function updateDetection(message) {
    const level = message.dangerous_level;
    const distance = message.distance;
    const position = message.position;

    console.log(`Indice pericolosità: ${level}, ${distance}, ${position}`);

    const indicator = document.getElementById('danger-level-indicator');
    const arrow = document.getElementById('arrow');

    if (level === 1) {
        indicator.style.backgroundColor = 'green';
    } else if (level === 2) {
        indicator.style.backgroundColor = 'yellow';
    } else if (level === 3) {
        indicator.style.backgroundColor = 'red';
    } else {
        indicator.style.backgroundColor = 'black';
    }

    if (position === 'right') {
        arrow.textContent = '▶';
    } else if (position === 'left') {
        arrow.textContent = '◀';
    } else if (position === 'back') {
        arrow.textContent = '▼';
    } else {
        arrow.textContent = '';
    }
}

// Connessione a ROSBridge WebSocket
const ros = new ROSLIB.Ros({
    url: 'ws://localhost:9090'  // Port
});

ros.on('connection', () => {
    console.log('Connesso a ROSBridge');
});

ros.on('error', (error) => {
    console.error('Errore di connessione:', error);
});

ros.on('close', () => {
    console.log('Connessione chiusa');
});

const mapTopic = new ROSLIB.Topic({
    ros: ros,
    name: '/gmap', 
    messageType: 'nav_msgs/OccupancyGrid' 
});

mapTopic.subscribe((message) => {
    processMapData(message);
});

const dangerousLevelTopic = new ROSLIB.Topic({
    ros: ros,
    name: '/backward_collision',
    messageType: 'slam_robot/backward_collision'
});

dangerousLevelTopic.subscribe((message) => {
    updateDetection(message);
});
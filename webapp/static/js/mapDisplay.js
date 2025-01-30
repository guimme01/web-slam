const canvas = document.getElementById('mapCanvas');
const ctx = canvas.getContext('2d');

const img = document.getElementById('image');

function processMapData(mapMsg) {
    console.log("MAPPA RICEVUTA");
    const width = mapMsg.info.width;
    const height = mapMsg.info.height;
    console.log(width);
    console.log(height);
    const data = mapMsg.data;

    canvas.width = width;
    canvas.height = height;

    const imgData = ctx.createImageData(width, height);

    for (let i = 0; i < data.length; i++) {
        const value = data[i];
        const color = value === 0 ? 255 : value === 100 ? 0 : 127;
        imgData.data[i * 4] = color;
        imgData.data[i * 4 + 1] = color;
        imgData.data[i * 4 + 2] = color;
        imgData.data[i * 4 + 3] = 255;
    }

    ctx.putImageData(imgData, 0, 0);
}



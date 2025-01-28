import axios from "axios";

interface sensorData {
  sensor1: string;
  sensor2: string;
  sensor3: string;
  sensor4: string;
  network: string;
}

const generateSensorData = (): sensorData => {
  const getRandomValue = () => (Math.random() * 200).toFixed(0);
  const getRandomNetworkStatus = () => (Math.random() > 0.5 ? "true" : "false");

  return {
    sensor1: getRandomValue(),
    sensor2: getRandomValue(),
    sensor3: getRandomValue(),
    sensor4: getRandomValue(),
    network: getRandomNetworkStatus(),
  };
};

// console.log(generateSensorData());

const sendData = async (): Promise<void> => {
  try {
    const sensorData = generateSensorData();
    const url = `http://localhost:3000/api/create-data?sensor1=${sensorData.sensor1}&sensor2=${sensorData.sensor2}&sensor3=${sensorData.sensor3}&sensor4=${sensorData.sensor4}&network=${sensorData.network}`;
    const responsne = await axios.get(url);
    console.log(responsne.data);
  } catch (error: unknown) {
    console.error(`[Error sending data]: ${error.message}`);
  }
};

setInterval(() => {
  sendData();
}, 1000);

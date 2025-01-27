import { Context } from "hono";
import Sensor, { ISensor } from "../models/sensorModel";

export const createSensorData = async (c: Context) => {
  try {
    const { sensor1, sensor2, sensor3, sensor4, network } = c.req.query() as {
      sensor1?: string;
      sensor2?: string;
      sensor3?: string;
      sensor4?: string;
      network?: string;
    };

    const networkValue = network === "false" ? false : true;

    if (!sensor1 || !sensor2 || !sensor3 || !sensor4) {
      return c.json({
        success: false,
        message: "All sensor values (sensor1, sensor2, sensor3, sensor4) must be provided",
      })
    }

    const sensorData: Partial<ISensor> = {
      sensor1,
      sensor2,
      sensor3,
      sensor4,
      network: networkValue,
      savedAt: new Date(),
    };

    await Sensor.create(sensorData)

    console.log(sensorData);

    
    return c.json({
      success: true,
      message: "Sensor data inserted successfully",
    });
  } catch (error) {
    console.error(error);
    return c.json({ error: "Internal Server Error" });
  }
};

export const getSensorData = async (c: Context) => {
  try {
    // const { sensor, network } = c.req.query;

    // Build a query object based on provided filters
    // const query: Partial<ISensor> = {};
    // if (sensor) {
    //   query.sensor = sensor;
    // }
    // if (network !== undefined) {
    //   query.network = network === "true";
    // }

    const sensors = await Sensor.find();

    return c.json({ success: true, data: sensors });
  } catch (error) {
    console.error(error);
    c.status(500);
    return c.json({ error: "Internal Server Error" });
  }
};

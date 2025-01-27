import { Hono } from "hono";
import {
  createSensorData,
  getSensorData,
} from "../controllers/sensorController";

const sensorDatas = new Hono();

sensorDatas.get("/", getSensorData);
sensorDatas.get("/create-data", createSensorData);

export default sensorDatas;

import { Hono } from "hono";
import { timing } from "hono/timing";
import { logger } from "hono/logger";
import { prettyJSON } from "hono/pretty-json";
import connectDB from "./config/connectDB";
import sensorDatas from "./routes/sensorRoutes";

const app = new Hono();

app.use("*", timing());
app.use("*", logger(), prettyJSON());

connectDB();

app.get("/", (c) => {
  return c.json({ app: "hono app" });
});

app.route("/api", sensorDatas);

export default app;

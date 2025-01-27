import { Document, model, Schema } from "mongoose";

export interface ISensor extends Document {
  sensor1: string;
  sensor2: string;
  sensor3: string;
  sensor4: string;
  network: boolean;
  savedAt: Date;
}

const sensorSchema = new Schema<ISensor>(
  {
    sensor1: {
      type: String,
      required: true,
    },
    sensor2: {
      type: String,
      required: true,
    },
    sensor3: {
      type: String,
      required: true,
    },
    sensor4: {
      type: String,
      required: true,
    },
    network: {
      type: Boolean,
      required: true,
    },
    savedAt: {
      type: Date,
      default: Date.now,
    },
  },
  {
    timestamps: true,
  }
);

// Middleware to set `savedAt` before saving
sensorSchema.pre<ISensor>("save", function (next) {
  this.savedAt = new Date();
  next();
});

const Sensor = model<ISensor>("sensor", sensorSchema);
export default Sensor;

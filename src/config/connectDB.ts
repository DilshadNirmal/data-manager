import mongoose from "mongoose";

const connectDB = async () => {
  try {
    if (Bun.env.MONGODB_URI !== undefined) {
      const conn = await mongoose.connect(`${Bun.env.MONGODB_URI}sensor-data`, {
        autoIndex: true,
      });

      console.log(`[MongoDB connected]: ${conn.connection.host}`);
    }
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

export default connectDB;

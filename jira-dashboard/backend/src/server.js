const express = require("express");
const { Pool } = require("pg");

const port = Number(process.env.PORT || 3001);
const pool = process.env.DATABASE_URL
  ? new Pool({
      connectionString: process.env.DATABASE_URL,
      connectionTimeoutMillis: 1000,
      max: 1,
    })
  : null;

if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error("PORT must be an integer between 1 and 65535");
}

function createApp(checkDatabase = defaultDatabaseCheck) {
  const app = express();

  app.get("/health", (_request, response) => {
    response.status(200).json({ status: "ok" });
  });

  app.get("/ready", async (_request, response) => {
    try {
      const databaseReady = await checkDatabase();
      if (!databaseReady) {
        return response
          .status(503)
          .json({ status: "not_ready", checks: { database: "unavailable" } });
      }

      return response
        .status(200)
        .json({ status: "ready", checks: { database: "available" } });
    } catch (error) {
      const code =
        error && typeof error === "object" && "code" in error
          ? error.code
          : "unknown";
      console.error(`Database readiness check failed (${code})`);
      return response
        .status(503)
        .json({ status: "not_ready", checks: { database: "unavailable" } });
    }
  });

  return app;
}

async function defaultDatabaseCheck() {
  if (!pool) {
    return false;
  }

  try {
    await pool.query("SELECT 1");
    return true;
  } catch (error) {
    const code =
      error && typeof error === "object" && "code" in error
        ? error.code
        : "unknown";
    console.error(`Database readiness check failed (${code})`);
    return false;
  }
}

if (require.main === module) {
  const app = createApp();
  app.listen(port, () => {
    console.log(`Backend listening on port ${port}`);
  });
}

module.exports = { createApp };
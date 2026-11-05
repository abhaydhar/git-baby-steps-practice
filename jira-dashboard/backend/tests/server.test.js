const assert = require("node:assert/strict");
const { after, before, describe, it } = require("node:test");
const { createApp } = require("../src/server");

describe("health and readiness endpoints", () => {
  let server;
  let baseUrl;

  before(async () => {
    server = createApp(async () => true).listen(0);
    await new Promise((resolve, reject) => {
      server.once("listening", resolve);
      server.once("error", reject);
    });
    baseUrl = `http://127.0.0.1:${server.address().port}`;
  });

  after(async () => {
    await new Promise((resolve, reject) => {
      server.close((error) => (error ? reject(error) : resolve()));
    });
  });

  it("reports process liveness", async () => {
    const response = await fetch(`${baseUrl}/health`);

    assert.equal(response.status, 200);
    assert.deepEqual(await response.json(), { status: "ok" });
  });

  it("reports readiness when PostgreSQL is available", async () => {
    const response = await fetch(`${baseUrl}/ready`);

    assert.equal(response.status, 200);
    assert.deepEqual(await response.json(), {
      status: "ready",
      checks: { database: "available" },
    });
  });

  it("reports not-ready when PostgreSQL is unavailable", async () => {
    const app = createApp(async () => false);
    const unavailableServer = app.listen(0);
    await new Promise((resolve, reject) => {
      unavailableServer.once("listening", resolve);
      unavailableServer.once("error", reject);
    });

    try {
      const response = await fetch(
        `http://127.0.0.1:${unavailableServer.address().port}/ready`,
      );

      assert.equal(response.status, 503);
      assert.deepEqual(await response.json(), {
        status: "not_ready",
        checks: { database: "unavailable" },
      });
    } finally {
      await new Promise((resolve, reject) => {
        unavailableServer.close((error) => (error ? reject(error) : resolve()));
      });
    }
  });
});

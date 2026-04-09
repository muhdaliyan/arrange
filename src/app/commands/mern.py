"""stup mern — MongoDB + Express + React + Node full-stack scaffold."""

from app.utils import (
    check_node,
    create_dirs,
    print_banner,
    print_done,
    run,
    write_file,
)

# ── Server templates ─────────────────────────────────────────────────

SERVER_INDEX = '''\
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api", require("./routes/api"));

// Health check
app.get("/health", (req, res) => res.json({ status: "ok" }));

// Connect to MongoDB & start server
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    console.log("✓ Connected to MongoDB");
    app.listen(PORT, () => console.log(`✓ Server running on port ${PORT}`));
  })
  .catch((err) => console.error("✗ MongoDB connection error:", err));
'''

SERVER_ROUTES_API = '''\
const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
  res.json({ message: "API is working!" });
});

module.exports = router;
'''

SERVER_MODELS_EXAMPLE = '''\
const mongoose = require("mongoose");

const ExampleSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    description: { type: String, default: "" },
  },
  { timestamps: true }
);

module.exports = mongoose.model("Example", ExampleSchema);
'''

SERVER_CONFIG_DB = '''\
const mongoose = require("mongoose");

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log("MongoDB connected");
  } catch (error) {
    console.error("MongoDB connection failed:", error.message);
    process.exit(1);
  }
};

module.exports = connectDB;
'''

ROOT_PACKAGE_JSON = '''\
{
  "name": "mern-app",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "server": "cd server && node index.js",
    "client": "cd client && npm run dev",
    "dev": "npx concurrently \\"npm run server\\" \\"npm run client\\""
  },
  "devDependencies": {
    "concurrently": "^8.0.0"
  }
}
'''

ENV_FILE = '''\
PORT=5000
MONGO_URI=mongodb://localhost:27017/myapp
NODE_ENV=development
'''


def run_command() -> None:
    """Scaffold a MERN stack project."""
    print_banner("mern", "MongoDB + Express + React + Node")

    check_node()

    # ── Server ───────────────────────────────────────────────────────
    create_dirs("server/routes", "server/models", "server/config", "server/middleware")

    run("npm init -y", cwd="server")
    run("npm install express mongoose dotenv cors", cwd="server")

    write_file("server/index.js", SERVER_INDEX)
    write_file("server/routes/api.js", SERVER_ROUTES_API)
    write_file("server/models/Example.js", SERVER_MODELS_EXAMPLE)
    write_file("server/config/db.js", SERVER_CONFIG_DB)

    # ── Client ───────────────────────────────────────────────────────
    run("npx -y create-vite@latest client --template react")
    run("npm install", cwd="client")
    run("npm install react-router-dom axios", cwd="client")

    # ── Root config ──────────────────────────────────────────────────
    write_file("package.json", ROOT_PACKAGE_JSON)
    run("npm install")
    write_file(".env", ENV_FILE)

    print_done()

const express = require("express");
const { exec } = require("child_process");
const cors = require("cors");

const app = express();

app.use(express.json());
app.use(cors());

/**
 * Executes a Python script with the given message as argument.
 * @param {string} message - The message to pass to the Python script.
 * @returns {Promise<string>} - The stdout from the script.
 */
const reqToExecutePythonScript = (message) => {
  return new Promise((resolve, reject) => {
    const safeMessage = message.replace(/"/g, '\\"'); // prevent injection
    const command = `python3 RAG.py ask "${safeMessage}"`;


    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`❌ Error: ${error.message}`);
        return reject(error);
      }

      if (stderr) {
        console.error(`⚠️ stderr: ${stderr}`);
        // Sometimes stderr contains warnings; don't reject unless stdout is empty
        if (!stdout) return reject(new Error(stderr));
      }

      console.log(`✅ stdout: ${stdout}`);
      resolve(stdout.trim());
    });
  });
};

// API endpoint to receive a message and return Python script's response
app.post("/feed-message", async (req, res) => {
  try {
    const { message } = req.body;

    console.log("message ............", message)

    if (!message || typeof message !== "string") {
      return res.status(400).json({ message: "", error: "Invalid message input" });
    }

    console.log("🔄 Generating response...");
    const result = await reqToExecutePythonScript(message);
    res.status(200).json({ message: result, error: "" });
  } catch (err) {
    console.error("❌ API failed:", err);
    res.status(500).json({ message: "", error: "Failed to process request" });
  }
});

// Start the server
const PORT = process.env.PORT || 8001;
app.listen(PORT, () => {
  console.log(`🚀 Server is running on port ${PORT}`);
});

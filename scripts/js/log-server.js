/**
 * Simple log server for Clauducky
 * 
 * This server provides endpoints for saving console logs from a web application.
 * Run this server alongside your web application to capture and save logs.
 * 
 * Usage:
 *   node log-server.js [port]
 * 
 * Default port is 3000 if not specified.
 */

const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = process.argv[2] || 3000;

// Enable CORS for all routes
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  next();
});

// Use express.json middleware
app.use(express.json({ limit: '10mb' }));

// Define paths for logs
// Use a path relative to clauducky directory for proper submodule usage
const logsDir = path.join(__dirname, '../../logs');
const currentLogPath = path.join(logsDir, 'console-log.txt');

// Ensure logs directory exists
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
  console.log(`Created logs directory at ${logsDir}`);
}

// Endpoint to save console logs
app.post('/api/save-logs', (req, res) => {
  if (!req.body || !req.body.log) {
    return res.status(400).send('No log data provided');
  }
  
  const logContent = req.body.log;
  const marker = req.body.marker || null;
  
  try {
    // Before overwriting current log, save it as previous log
    const previousLogPath = path.join(logsDir, 'previous-log.txt');
    
    // If current log exists, move it to previous
    if (fs.existsSync(currentLogPath)) {
      try {
        // Read current log content
        const currentContent = fs.readFileSync(currentLogPath, 'utf8');
        // Only save as previous if there's actual content
        if (currentContent.trim().length > 0) {
          fs.writeFileSync(previousLogPath, currentContent);
          console.log('Current log saved as previous-log.txt');
        }
      } catch (err) {
        console.error('Error saving previous log:', err.message);
      }
    }
    
    // Save as the current log file
    fs.writeFileSync(currentLogPath, logContent);
    console.log('Updated current log file');
    
    // If this is a session end or other marker, log it
    if (marker) {
      console.log(`Log marker: ${marker}`);
    }
    
    res.status(200).send('Logs saved successfully');
  } catch (error) {
    console.error('Error saving logs:', error.message);
    res.status(500).send(`Error saving logs: ${error.message}`);
  }
});

// Endpoint to check logs
app.get('/api/logs', (req, res) => {
  try {
    if (!fs.existsSync(currentLogPath)) {
      return res.status(200).json({ 
        exists: false, 
        message: 'No current log file exists' 
      });
    }
    
    const stats = fs.statSync(currentLogPath);
    const logContent = fs.readFileSync(currentLogPath, 'utf8');
    const logLines = logContent.split('\n');
    
    // Get log summary
    const errorCount = logLines.filter(line => 
      line.toLowerCase().includes('[error]') || line.toLowerCase().includes('[warn]')).length;
    
    const summary = {
      exists: true,
      size: stats.size,
      lines: logLines.length,
      errors: errorCount,
      lastModified: stats.mtime
    };
    
    res.status(200).json(summary);
  } catch (error) {
    console.error('Error checking logs:', error.message);
    res.status(500).send(`Error checking logs: ${error.message}`);
  }
});

// Endpoint to clear logs
app.post('/api/clear-logs', (req, res) => {
  try {
    if (fs.existsSync(currentLogPath)) {
      fs.writeFileSync(currentLogPath, '');
      console.log('Cleared current log file');
    }
    
    res.status(200).send('Logs cleared successfully');
  } catch (error) {
    console.error('Error clearing logs:', error.message);
    res.status(500).send(`Error clearing logs: ${error.message}`);
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Clauducky Log Server running at http://localhost:${port}`);
  console.log(`Logs will be saved to ${logsDir}`);
  console.log('Use Ctrl+C to stop the server');
  
  // Create an empty log file if it doesn't exist
  if (!fs.existsSync(currentLogPath)) {
    fs.writeFileSync(currentLogPath, '');
    console.log('Created empty current log file');
  }
});
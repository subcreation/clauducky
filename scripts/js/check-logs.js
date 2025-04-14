/**
 * Enhanced log checker script for Clauducky
 * Run this with: node check-logs.js [options]
 * 
 * Options:
 *   errors - Show only errors and warnings
 *   events - Show only event markers
 *   previous - View the previous log
 *   clear - Clear the current log (creates empty file)
 *   compare - Compare current and previous logs
 *   <none> - Default, show summary of current log
 */

const fs = require('fs');
const path = require('path');

// Process command line arguments
const arg = process.argv[2];

// Define paths
// Use a path relative to clauducky directory for proper submodule usage
const logsDir = path.join(__dirname, '../../logs');
const currentLogPath = path.join(logsDir, 'console-log.txt');
const previousLogPath = path.join(logsDir, 'previous-log.txt');

// Ensure logs directory exists
if (!fs.existsSync(logsDir)) {
  try {
    fs.mkdirSync(logsDir, { recursive: true });
    console.log(`Created logs directory at ${logsDir}`);
  } catch (err) {
    console.error(`Failed to create logs directory: ${err.message}`);
  }
}

// Helper function to get log files
function getLogFiles() {
  if (!fs.existsSync(logsDir)) {
    return [];
  }
  
  const files = [];
  
  // Check for current log
  if (fs.existsSync(currentLogPath)) {
    files.push({
      name: 'console-log.txt (Current)',
      path: currentLogPath,
      stats: fs.statSync(currentLogPath),
      isCurrent: true
    });
  }
  
  // Check for previous log
  if (fs.existsSync(previousLogPath)) {
    files.push({
      name: 'previous-log.txt',
      path: previousLogPath,
      stats: fs.statSync(previousLogPath),
      isPrevious: true
    });
  }
  
  // Return sorted files (current, previous)
  return files.map(file => ({ name: file.name, path: file.path, isCurrent: file.isCurrent, isPrevious: file.isPrevious }));
}

// Check if current log file exists
if (!fs.existsSync(currentLogPath)) {
  console.log('ℹ️ No current log file found. Creating empty log file.');
  try {
    fs.writeFileSync(currentLogPath, '');
  } catch (err) {
    console.error(`Failed to create log file: ${err.message}`);
    process.exit(1);
  }
}

// Read the log file if it exists
let logContent = '';
let logLines = [];
try {
  if (fs.existsSync(currentLogPath)) {
    logContent = fs.readFileSync(currentLogPath, 'utf8');
    logLines = logContent.split('\n');
  }
} catch (err) {
  console.error(`Error reading log file: ${err.message}`);
  process.exit(1);
}

// Handle viewing previous log
if (arg === 'previous') {
  if (!fs.existsSync(previousLogPath)) {
    console.log('ℹ️ No previous log file found.');
    process.exit(0);
  }
  
  try {
    const previousLog = fs.readFileSync(previousLogPath, 'utf8');
    console.log(`📜 Contents of previous log:`);
    console.log(previousLog);
  } catch (err) {
    console.error(`Error reading previous log: ${err.message}`);
    process.exit(1);
  }
  
  process.exit(0);
}

// Handle clearing logs
if (arg === 'clear') {
  try {
    // Clear current log file
    fs.writeFileSync(currentLogPath, '');
    console.log('✅ Current log file cleared successfully');
    process.exit(0);
  } catch (err) {
    console.error(`Error clearing log: ${err.message}`);
    process.exit(1);
  }
}

// Handle comparing current and previous logs
if (arg === 'compare') {
  if (!fs.existsSync(currentLogPath) || !fs.existsSync(previousLogPath)) {
    console.log('ℹ️ Need both current and previous logs to compare differences.');
    process.exit(0);
  }
  
  try {
    const currentLog = fs.readFileSync(currentLogPath, 'utf8').split('\n');
    const previousLog = fs.readFileSync(previousLogPath, 'utf8').split('\n');
    
    console.log(`📊 Comparing current log with previous log`);
    
    // Find lines that exist in current but not in previous
    const uniqueToCurrent = currentLog.filter(line => !previousLog.includes(line) && line.trim() !== '');
    // Find lines that exist in previous but not in current
    const uniqueToPrevious = previousLog.filter(line => !currentLog.includes(line) && line.trim() !== '');
    
    if (uniqueToCurrent.length === 0 && uniqueToPrevious.length === 0) {
      console.log('✅ The logs are identical!');
    } else {
      if (uniqueToCurrent.length > 0) {
        console.log(`\n➕ Lines unique to current log (${uniqueToCurrent.length}):`);
        uniqueToCurrent.slice(0, 20).forEach(line => console.log(`  ${line}`));
        if (uniqueToCurrent.length > 20) {
          console.log(`  ... and ${uniqueToCurrent.length - 20} more lines`);
        }
      }
      
      if (uniqueToPrevious.length > 0) {
        console.log(`\n➖ Lines unique to previous log (${uniqueToPrevious.length}):`);
        uniqueToPrevious.slice(0, 20).forEach(line => console.log(`  ${line}`));
        if (uniqueToPrevious.length > 20) {
          console.log(`  ... and ${uniqueToPrevious.length - 20} more lines`);
        }
      }
    }
  } catch (err) {
    console.error(`Error comparing logs: ${err.message}`);
    process.exit(1);
  }
  
  process.exit(0);
}

// Handle errors-only command
if (arg === 'errors') {
  const errorLines = logLines.filter(line => 
    line.toLowerCase().includes('[error]') || line.toLowerCase().includes('[warn]'));
  
  if (errorLines.length === 0) {
    console.log('✅ No errors or warnings found in the log!');
  } else {
    console.log(`⚠️ Found ${errorLines.length} errors or warnings:`);
    errorLines.forEach(line => console.log(line));
  }
  
  process.exit(0);
}

// Handle events-only command
if (arg === 'events') {
  const eventLines = logLines.filter(line => 
    line.includes('EVENT_MARKER') || line.includes('MARKER') || line.includes('Session'));
  
  if (eventLines.length === 0) {
    console.log('ℹ️ No event markers found in the log!');
  } else {
    console.log(`🚩 Found ${eventLines.length} event markers:`);
    eventLines.forEach(line => console.log(line));
  }
  
  process.exit(0);
}

// Default behavior: show log summary
const errorCount = logLines.filter(line => 
  line.toLowerCase().includes('[error]') || line.toLowerCase().includes('[warn]')).length;

const eventCount = logLines.filter(line => 
  line.includes('EVENT_MARKER') || line.includes('MARKER') || line.includes('Session')).length;

// Count log entries by type
const logCounts = {
  info: logLines.filter(line => line.toLowerCase().includes('[info]')).length,
  log: logLines.filter(line => line.toLowerCase().includes('[log]') && !line.toLowerCase().includes('[info]')).length,
  warn: logLines.filter(line => line.toLowerCase().includes('[warn]')).length,
  error: logLines.filter(line => line.toLowerCase().includes('[error]')).length,
  debug: logLines.filter(line => line.toLowerCase().includes('[debug]')).length
};

console.log('📋 Console Log Summary:');
console.log(`Total log entries: ${logLines.length}`);
console.log(`• Info: ${logCounts.info}`);
console.log(`• Log: ${logCounts.log}`);
console.log(`• Warn: ${logCounts.warn}`);
console.log(`• Error: ${logCounts.error}`);
console.log(`• Debug: ${logCounts.debug}`);
console.log(`• Event markers: ${eventCount}`);

if (errorCount > 0) {
  console.log(`\n⚠️ Found ${errorCount} errors or warnings. Use 'node check-logs.js errors' to view them.`);
}

if (eventCount > 0) {
  console.log(`\n🚩 Found ${eventCount} event markers. Use 'node check-logs.js events' to view them.`);
}

// Show the last 10 log entries
const lastLogs = logLines.filter(line => line.trim() !== '').slice(-10);
console.log('\n🔄 Last 10 log entries:');
lastLogs.forEach(line => console.log(line));
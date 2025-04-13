/**
 * Enhanced log checker script for Clauducky
 * Run this with: node check-logs.js [options]
 * 
 * Options:
 *   history - View log history and compare logs
 *   errors - Show only errors and warnings
 *   events - Show only event markers
 *   diff [log1] [log2] - Compare two log files (by index)
 *   <none> - Default, show summary of all logs
 */

const fs = require('fs');
const path = require('path');

// Process command line arguments
const arg = process.argv[2];

// Define paths
// Use a path relative to clauducky directory for proper submodule usage
const logsDir = path.join(__dirname, '../../logs');
const currentLogPath = path.join(logsDir, 'console-log.txt');

// Ensure logs directory exists
if (!fs.existsSync(logsDir)) {
  try {
    fs.mkdirSync(logsDir, { recursive: true });
    console.log(`Created logs directory at ${logsDir}`);
  } catch (err) {
    console.error(`Failed to create logs directory: ${err.message}`);
  }
}

// Helper function to get all log files sorted by date (newest first)
function getLogFiles() {
  if (!fs.existsSync(logsDir)) {
    return [];
  }
  
  return fs.readdirSync(logsDir)
    .filter(file => file.startsWith('log-') && file.endsWith('.txt'))
    .map(file => ({
      name: file,
      path: path.join(logsDir, file),
      stats: fs.statSync(path.join(logsDir, file))
    }))
    .sort((a, b) => b.stats.mtime.getTime() - a.stats.mtime.getTime()) // Newest first
    .map(file => ({ name: file.name, path: file.path }));
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

// Handle history command
if (arg === 'history') {
  const logFiles = getLogFiles();
  
  if (logFiles.length === 0) {
    console.log('ℹ️ No historical logs found in logs directory.');
    process.exit(0);
  }
  
  console.log(`📚 Found ${logFiles.length} historical logs:`);
  logFiles.forEach((file, index) => {
    console.log(`${index + 1}. ${file.name}`);
  });
  
  console.log('\nUse: node check-logs.js history [number] to view a specific log');
  
  // If a specific log is requested
  const logNumber = parseInt(process.argv[3]);
  if (!isNaN(logNumber) && logNumber > 0 && logNumber <= logFiles.length) {
    const historicalLog = fs.readFileSync(logFiles[logNumber - 1].path, 'utf8');
    console.log(`\n📜 Contents of ${logFiles[logNumber - 1].name}:`);
    console.log(historicalLog);
  }
  
  process.exit(0);
}

// Handle diff command
if (arg === 'diff') {
  const logFiles = getLogFiles();
  
  if (logFiles.length < 2) {
    console.log('ℹ️ Need at least 2 log files to compare differences.');
    process.exit(0);
  }
  
  const log1Index = parseInt(process.argv[3]) || 1;
  const log2Index = parseInt(process.argv[4]) || 2;
  
  if (log1Index < 1 || log1Index > logFiles.length || 
    log2Index < 1 || log2Index > logFiles.length) {
    console.log(`❌ Invalid log indices. Please use values between 1 and ${logFiles.length}.`);
    process.exit(1);
  }
  
  const log1 = fs.readFileSync(logFiles[log1Index - 1].path, 'utf8').split('\n');
  const log2 = fs.readFileSync(logFiles[log2Index - 1].path, 'utf8').split('\n');
  
  console.log(`📊 Comparing log ${log1Index} (${logFiles[log1Index - 1].name}) with log ${log2Index} (${logFiles[log2Index - 1].name})`);
  
  // Find lines that exist in log1 but not in log2
  const uniqueToLog1 = log1.filter(line => !log2.includes(line) && line.trim() !== '');
  // Find lines that exist in log2 but not in log1
  const uniqueToLog2 = log2.filter(line => !log1.includes(line) && line.trim() !== '');
  
  if (uniqueToLog1.length === 0 && uniqueToLog2.length === 0) {
    console.log('✅ The logs are identical!');
  } else {
    if (uniqueToLog1.length > 0) {
      console.log(`\n➖ Lines unique to log ${log1Index} (${uniqueToLog1.length}):`);
      uniqueToLog1.slice(0, 20).forEach(line => console.log(`  ${line}`));
      if (uniqueToLog1.length > 20) {
        console.log(`  ... and ${uniqueToLog1.length - 20} more lines`);
      }
    }
    
    if (uniqueToLog2.length > 0) {
      console.log(`\n➕ Lines unique to log ${log2Index} (${uniqueToLog2.length}):`);
      uniqueToLog2.slice(0, 20).forEach(line => console.log(`  ${line}`));
      if (uniqueToLog2.length > 20) {
        console.log(`  ... and ${uniqueToLog2.length - 20} more lines`);
      }
    }
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
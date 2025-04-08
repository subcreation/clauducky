/**
 * Script to clean up log files for Clauducky
 * 
 * Usage:
 *   node clear-logs.js [keep-count] [--clear-current] [--all]
 *   
 * Arguments:
 *   keep-count: Number of most recent log files to keep (default: 5)
 *   --clear-current: Also clear the current console-log.txt file
 *   --all: Remove ALL log files (overrides keep-count)
 */

const fs = require('fs');
const path = require('path');

// Directory containing log files
const logsDir = path.join(__dirname, '../../logs');
const currentLogPath = path.join(__dirname, '../../logs/console-log.txt');

// Process arguments
const clearAll = process.argv.includes('--all');
const clearCurrent = process.argv.includes('--clear-current') || clearAll;
const keepCount = clearAll ? 0 : (parseInt(process.argv[2]) || 5);

// Clear the current log file if requested
if (clearCurrent && fs.existsSync(currentLogPath)) {
  fs.writeFileSync(currentLogPath, '');
  console.log('✅ Current log file cleared successfully');
}

// Ensure the logs directory exists
if (!fs.existsSync(logsDir)) {
  console.log('ℹ️ No logs directory found. Creating empty logs directory.');
  try {
    fs.mkdirSync(logsDir, { recursive: true });
  } catch (err) {
    console.error(`Failed to create logs directory: ${err.message}`);
    process.exit(1);
  }
  process.exit(0);
}

try {
  // Get all log files
  const files = fs.readdirSync(logsDir)
    .filter(file => file.startsWith('log-') && file.endsWith('.txt'))
    .map(file => ({
      name: file,
      path: path.join(logsDir, file),
      stats: fs.statSync(path.join(logsDir, file))
    }))
    .sort((a, b) => b.stats.mtime.getTime() - a.stats.mtime.getTime()); // Sort by modification time, newest first

  // Keep only the specified number of most recent files
  if (files.length <= keepCount && !clearAll) {
    console.log(`ℹ️ Only ${files.length} log files exist, keeping all (requested to keep ${keepCount}).`);
    process.exit(0);
  }

  // Delete older files
  const filesToDelete = clearAll ? files : files.slice(keepCount);
  console.log(`🗑️ Deleting ${filesToDelete.length} log files...`);
  
  let deletedCount = 0;
  for (const file of filesToDelete) {
    fs.unlinkSync(file.path);
    deletedCount++;
  }

  if (clearAll) {
    console.log(`✅ Deleted ALL log files (${deletedCount} total)`);
  } else {
    console.log(`✅ Deleted ${deletedCount} log files. Kept the ${keepCount} most recent.`);
  }
} catch (error) {
  console.error('❌ Error cleaning log files:', error.message);
  process.exit(1);
}
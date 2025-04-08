/**
 * Clauducky Console Logger
 * 
 * This script captures browser console output and saves it to a file for analysis by Claude Code.
 * It provides a mechanism to capture logs, warnings, errors, and other console messages
 * from a web application, with support for custom markers to identify key events.
 */

(function() {
  // Create a div to display logs (hidden by default, can be toggled with Alt+C)
  const consoleContainer = document.createElement('div');
  consoleContainer.id = 'clauducky-console-output';
  consoleContainer.style.cssText = 'position: fixed; bottom: 0; right: 0; width: 500px; height: 300px; background: rgba(0,0,0,0.8); color: white; overflow: auto; font-family: monospace; font-size: 12px; padding: 10px; z-index: 9999; display: none;';
  document.body.appendChild(consoleContainer);
  
  // Add a button to toggle console display (hidden but accessible via keyboard shortcut)
  const toggleButton = document.createElement('button');
  toggleButton.textContent = 'Toggle Console';
  toggleButton.style.cssText = 'position: fixed; bottom: 0; right: 0; z-index: 10000; padding: 5px; opacity: 0; pointer-events: none;';
  toggleButton.addEventListener('click', () => {
    consoleContainer.style.display = consoleContainer.style.display === 'none' ? 'block' : 'none';
  });
  document.body.appendChild(toggleButton);
  
  // Add keyboard shortcut Alt+C to toggle console
  document.addEventListener('keydown', (e) => {
    if (e.altKey && e.key === 'c') {
      consoleContainer.style.display = consoleContainer.style.display === 'none' ? 'block' : 'none';
    }
  });
  
  // Create storage for logs
  let logData = [];
  const logFile = 'console-log.txt';
  
  // Store original console methods
  const originalConsole = {
    log: console.log,
    warn: console.warn,
    error: console.error,
    info: console.info,
    debug: console.debug
  };
  
  // Function to format log entry
  function formatLogEntry(type, args) {
    const timestamp = new Date().toISOString();
    return `[${timestamp}] [${type}] ${Array.from(args).map(arg => {
      try {
        return typeof arg === 'object' ? JSON.stringify(arg) : String(arg);
      } catch (e) {
        return '[Object]';
      }
    }).join(' ')}`;
  }
  
  // Server API endpoint for logs
  const LOG_ENDPOINT = '/api/save-logs';
  
  // Function to add log to display and save to memory
  function processLog(type, args) {
    const logEntry = formatLogEntry(type, args);
    
    // Add to visual display
    const logElement = document.createElement('div');
    logElement.className = `log-${type}`;
    logElement.style.cssText = type === 'error' ? 'color: #ff5555;' : (type === 'warn' ? 'color: #ffff55;' : 'color: #aaaaff;');
    logElement.textContent = logEntry;
    consoleContainer.appendChild(logElement);
    consoleContainer.scrollTop = consoleContainer.scrollHeight;
    
    // Store log in memory
    logData.push(logEntry);
    
    // Save to localStorage as well for backup
    localStorage.setItem('clauducky-console-logs', JSON.stringify(logData));
    
    return logEntry;
  }
  
  // Override console methods
  console.log = function() {
    const logEntry = window.processLog('log', arguments);
    originalConsole.log.apply(console, arguments);
    return logEntry;
  };
  
  console.warn = function() {
    const logEntry = window.processLog('warn', arguments);
    originalConsole.warn.apply(console, arguments);
    return logEntry;
  };
  
  console.error = function() {
    const logEntry = window.processLog('error', arguments);
    originalConsole.error.apply(console, arguments);
    return logEntry;
  };
  
  console.info = function() {
    const logEntry = window.processLog('info', arguments);
    originalConsole.info.apply(console, arguments);
    return logEntry;
  };
  
  console.debug = function() {
    const logEntry = window.processLog('debug', arguments);
    originalConsole.debug.apply(console, arguments);
    return logEntry;
  };
  
  // Capture uncaught errors
  window.addEventListener('error', function(event) {
    console.error('Uncaught error:', event.error.message);
  });
  
  // Export logs button (hidden but accessible via keyboard shortcut)
  const exportButton = document.createElement('button');
  exportButton.textContent = 'Export Logs';
  exportButton.style.cssText = 'position: fixed; bottom: 0; right: 100px; z-index: 10000; padding: 5px; opacity: 0; pointer-events: none;';
  exportButton.addEventListener('click', () => {
    saveLogsToFile();
  });
  document.body.appendChild(exportButton);
  
  // Add keyboard shortcut Alt+E to export logs
  document.addEventListener('keydown', (e) => {
    if (e.altKey && e.key === 'e') {
      exportButton.click();
    }
  });
  
  // Clear logs button (hidden but accessible via keyboard shortcut)
  const clearButton = document.createElement('button');
  clearButton.textContent = 'Clear Logs';
  clearButton.style.cssText = 'position: fixed; bottom: 0; right: 200px; z-index: 10000; padding: 5px; opacity: 0; pointer-events: none;';
  clearButton.addEventListener('click', () => {
    logData = [];
    localStorage.removeItem('clauducky-console-logs');
    consoleContainer.innerHTML = '';
    console.log('Logs cleared');
  });
  document.body.appendChild(clearButton);
  
  // Add keyboard shortcut Alt+X to clear logs
  document.addEventListener('keydown', (e) => {
    if (e.altKey && e.key === 'x') {
      clearButton.click();
    }
  });
  
  // Function to save logs to file
  function saveLogsToFile(marker = null) {
    if (logData.length === 0) {
      console.warn('No logs to save');
      return;
    }
    
    let logContent = logData.join('\n');
    
    // Add marker if provided
    if (marker) {
      logContent += `\n${marker}\n`;
    }
    
    // Try to save to server if available
    if (typeof fetch !== 'undefined') {
      try {
        fetch(LOG_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            log: logContent,
            marker: marker
          })
        }).catch(err => {
          console.warn('Failed to save logs to server:', err.message);
          downloadLogsAsFile(logContent);
        });
        console.log('Logs sent to server');
      } catch (e) {
        console.warn('Error saving logs to server:', e.message);
        downloadLogsAsFile(logContent);
      }
    } else {
      downloadLogsAsFile(logContent);
    }
  }
  
  // Fallback function to download logs as a file
  function downloadLogsAsFile(content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'clauducky-console-log.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    console.log('Logs saved as download');
  }
  
  // Add custom marker functions
  window.clauduckyLogs = {
    // Save logs with a marker
    saveWithMarker: function(marker) {
      console.log(`Adding marker: ${marker}`);
      saveLogsToFile(marker);
    },
    
    // Start a new logging session with a marker
    startSession: function(sessionName) {
      // Clear existing logs
      logData = [];
      localStorage.removeItem('clauducky-console-logs');
      consoleContainer.innerHTML = '';
      
      // Log session start
      console.log(`Starting logging session: ${sessionName}`);
    },
    
    // End the current logging session with a marker
    endSession: function(sessionName) {
      console.log(`Ending logging session: ${sessionName}`);
      saveLogsToFile(`SESSION_END_MARKER: ${sessionName}`);
    },
    
    // Mark a specific event in the logs
    markEvent: function(eventName) {
      console.log(`EVENT_MARKER: ${eventName}`);
    },
    
    // Clear all logs
    clear: function() {
      logData = [];
      localStorage.removeItem('clauducky-console-logs');
      consoleContainer.innerHTML = '';
      console.log('Logs cleared');
    }
  };
  
  // Make processLog available globally but don't send to server immediately
  window.processLog = function(type, args) {
    // Just store logs in memory - don't send to server for each log entry
    const logEntry = processLog(type, args);
    return logEntry;
  };
  
  console.log('Clauducky Console Logger initialized');
})();

// Export Node.js module for server-side use
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
  module.exports = {
    saveLogs: function(logContent, filePath) {
      const fs = require('fs');
      const path = require('path');
      
      // Create logs directory if it doesn't exist
      const logsDir = path.dirname(filePath);
      if (!fs.existsSync(logsDir)) {
        fs.mkdirSync(logsDir, { recursive: true });
      }
      
      // Write logs to file
      fs.writeFileSync(filePath, logContent);
      return true;
    }
  };
}
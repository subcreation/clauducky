#!/bin/bash
# Test script for ducky_debug.py

# Change to the script directory
cd "$(dirname "$0")"

# Test the ducky debug script with a simple error
echo "Testing ducky_debug.py with OpenAI..."
python python/ducky_debug.py "TypeError: Cannot read property 'map' of undefined at line 42 in UserList.jsx" --code "function UserList({ users }) {
  return (
    <div>
      <h2>User List</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}" --output text

# Test with Anthropic if you want to try both
# echo -e "\n\nTesting with Anthropic..."
# python python/ducky_debug.py "TypeError: Cannot read property 'map' of undefined at line 42 in UserList.jsx" --provider anthropic --model claude-3-haiku-20240307 --output text
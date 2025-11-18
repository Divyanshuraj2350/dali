
#!/bin/bash

# Dali Voice Assistant Startup Script
echo "🤖 Starting Dali Voice Assistant..."

# Navigate to dali directory
cd ~/dali

# Run the service
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 dali_service.py

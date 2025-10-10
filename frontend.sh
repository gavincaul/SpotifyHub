
#!/bin/bash
if lsof -i :3000 >/dev/null; then 
    echo "Port 3000 in use. Killing existing process..." 
    kill -9 $(lsof -t -i :3000) 
fi 
cd src/frontend
npm run start

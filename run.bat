@echo off
chcp 65001 >nul
cd /d "C:\Users\Username\Desktop\кутьков"

echo Stopping old containers...
docker stop monitor 2>nul
docker rm monitor 2>nul

echo Building Docker image...
docker build -t website-monitor .

echo Starting container...
docker run -d -p 8000:8000 --name monitor website-monitor

echo.
echo ✅ Container started!
echo 🌐 Open http://localhost:8000/docs in your browser
echo.
echo Commands:
echo   docker ps              - check status
echo   docker logs monitor    - view logs
echo   docker stop monitor    - stop container
echo.
pause
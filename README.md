# Browser Remote Control System

A DIY "Browser.lol" style system to remotely control your home laptop via a web browser.

## Part 1: The Server (Railway)

The `server` folder contains the Node.js application that you upload to Railway. It provides the web interface and routes the video/mouse data.

1. Upload this repository to your GitHub account.
2. Go to [Railway.app](https://railway.app), create a new project from your GitHub repo.
3. Set the root directory to `/server` if Railway doesn't auto-detect it.
4. Get your public Railway URL once it deploys.

## Part 2: The Agent (Home Laptop)

The `agent` folder contains a Python script that you leave running on your home laptop.

1. Open `agent/agent.py` and replace `SERVER_URL` with your Railway URL.
2. Open a terminal on your home laptop and install the dependencies:
   ```bash
   pip install -r agent/requirements.txt
   ```
3. Run the script:
   ```bash
   python agent/agent.py
   ```

Now you can open your Railway URL on any computer, double-click to go full-screen, and use your home laptop seamlessly!

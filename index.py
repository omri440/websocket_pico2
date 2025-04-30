<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Live Temperature Dashboard</title>
  <style>
    body {
      background-color: #1c1c1c;
      color: white;
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      padding: 0;
    }

    header {
      display: flex;
      align-items: center;
      padding: 10px 20px;
      background-color: #2b2b2b;
    }

    header img {
      height: 30px;
      margin-right: 10px;
    }

    header h1 {
      color: limegreen;
      font-size: 1.5em;
    }

    .container {
      display: flex;
      justify-content: space-around;
      align-items: center;
      padding: 40px;
      flex-wrap: wrap;
    }

    .gauge {
      width: 200px;
      height: 200px;
      border-radius: 50%;
      background: conic-gradient(green 0% 60%, orange 60% 85%, red 85% 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      margin-bottom: 20px;
    }

    .gauge span {
      font-size: 2.5em;
      font-weight: bold;
      color: white;
    }

    .gauge label {
      position: absolute;
      bottom: 20px;
      font-size: 0.9em;
      color: #ccc;
    }

    #chartContainer {
      width: 100%;
      max-width: 700px;
      height: 400px;
    }

    h2 {
      text-align: center;
    }

    canvas {
      background-color: #121212;
    }

    .button-panel {
      text-align: center;
      margin-top: 20px;
    }

    .button-panel button {
      background-color: #444;
      color: white;
      border: none;
      padding: 10px 15px;
      margin: 5px;
      font-size: 1em;
      border-radius: 5px;
      cursor: pointer;
    }

    .button-panel button:hover {
      background-color: #666;
    }
  </style>
</head>
<body>
  <header>
    <img src="https://upload.wikimedia.org/wikipedia/en/c/cb/Raspberry_Pi_Logo.svg" alt="Raspberry Pi">
    <h1>Live Temperature Dashboard</h1>
  </header>

  <h2>Temperature: <span id="tempValue">--</span> °C</h2>

  <div class="button-panel">
    <button onclick="toggleLed('ledRed', 1)">🔴 Red ON</button>
    <button onclick="toggleLed('ledRed', 0)">⚫ Red OFF</button>
    <button onclick="toggleLed('ledGreen', 1)">🟢 Green ON</button>
    <button onclick="toggleLed('ledGreen', 0)">⚫ Green OFF</button>
    <br><br>
    <button onclick="toggleAlarm(true)">🔔 Arm Alarm</button>
    <button onclick="toggleAlarm(false)">🔕 Disarm Alarm</button>
    <p id="alarmStatus">Alarm Status: --</p>
  </div>

  <div class="container">
    <div class="gauge">
      <span id="gaugeTemp">--</span>
      <label>Bedroom</label>
    </div>
    <div id="chartContainer">
      <canvas id="tempChart"></canvas>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    // ✅ יצירת WebSocketים לפני כל שימוש
    const ws = new WebSocket("ws://" + location.host + "/control");
    const alarmWS = new WebSocket("ws://" + location.host + "/alarm");

    // ✅ פונקציות לשליטה על הלדים והאזעקה
    function toggleLed(ledName, state) {
      const message = {};
      message[ledName] = state;
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(message));
      } else {
        console.log("WebSocket not connected.");
      }
    }

    function toggleAlarm(state) {
      if (alarmWS.readyState === WebSocket.OPEN) {
        alarmWS.send(JSON.stringify({ alarm: state }));
        document.getElementById("alarmStatus").textContent = state ? "Alarm Status: Armed" : "Alarm Status: Disarmed";
      }
    }

    // ✅ התראה על תנועה
    alarmWS.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.event === "motion_detected") {
        alert("🚨 Motion Detected!");
      }
    };

    // ✅ קבלת טמפרטורה
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const temp = data.temperature;
      const now = new Date().toLocaleTimeString();

      chart.data.labels.push(now);
      chart.data.datasets[0].data.push(temp);
      if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
      }

      document.getElementById('tempValue').textContent = temp.toFixed(2);
      document.getElementById('gaugeTemp').textContent = temp.toFixed(2);
      chart.update();
    };

    ws.onerror = () => {
      document.getElementById('tempValue').textContent = 'Error';
      document.getElementById('gaugeTemp').textContent = 'Error';
    };

    // ✅ יצירת גרף
    const ctx = document.getElementById('tempChart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: 'Temperature (°C)',
          data: [],
          borderColor: 'limegreen',
          backgroundColor: 'transparent',
          pointRadius: 2,
          tension: 0.2,
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            min: 25,
            max: 50,
            ticks: { color: "#ccc" },
            grid: { color: "#444" }
          },
          x: {
            ticks: { color: "#ccc" },
            grid: { color: "#444" }
          }
        },
        plugins: {
          legend: {
            labels: { color: 'white' }
          }
        }
      }
    });
  </script>
</body>
</html>

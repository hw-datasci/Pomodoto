// DOM elements
const minutesElement = document.getElementById("minutes");
const secondsElement = document.getElementById("seconds");
const startButton = document.getElementById("start-btn");
const pauseButton = document.getElementById("pause-btn");
const resetButton = document.getElementById("reset-btn");
const pomodoroButton = document.getElementById("pomodoro-btn");
const shortBreakButton = document.getElementById("short-break-btn");
const longBreakButton = document.getElementById("long-break-btn");
const sessionCountElement = document.getElementById("session-count");
const settingsButton = document.getElementById("settings-btn");
const settingsPanel = document.getElementById("settings-panel");
const saveSettingsButton = document.getElementById("save-settings-btn");
const notificationSound = document.getElementById("notification-sound");

// Timer settings
let settings = {
  pomodoroTime: 25,
  shortBreakTime: 5,
  longBreakTime: 15,
  autoStartBreaks: false,
  autoStartPomodoros: false,
};

// Timer variables
let timerInterval = null;
let minutes = settings.pomodoroTime;
let seconds = 0;
let isRunning = false;
let currentMode = "pomodoro";
let sessionCount = 0;

// Initialize the timer display
function updateTimerDisplay() {
  minutesElement.textContent = minutes.toString().padStart(2, "0");
  secondsElement.textContent = seconds.toString().padStart(2, "0");
}

// Timer functionality
function startTimer() {
  if (!isRunning) {
    isRunning = true;
    startButton.disabled = true;
    pauseButton.disabled = false;

    timerInterval = setInterval(() => {
      if (seconds === 0) {
        if (minutes === 0) {
          clearInterval(timerInterval);
          isRunning = false;
          notificationSound.play();
          completeTimer();
          return;
        }
        minutes--;
        seconds = 59;
      } else {
        seconds--;
      }
      updateTimerDisplay();
      updateDocumentTitle();
    }, 1000);
  }
}

function pauseTimer() {
  if (isRunning) {
    clearInterval(timerInterval);
    isRunning = false;
    startButton.disabled = false;
    pauseButton.disabled = true;
  }
}

function resetTimer() {
  clearInterval(timerInterval);
  isRunning = false;
  setTimerForMode(currentMode);
  updateTimerDisplay();
  startButton.disabled = false;
  pauseButton.disabled = true;
  updateDocumentTitle();
}

function updateDocumentTitle() {
  document.title = `${minutesElement.textContent}:${
    secondsElement.textContent
  } - ${currentMode === "pomodoro" ? "Focus" : "Break"}`;
}

function completeTimer() {
  if (currentMode === "pomodoro") {
    sessionCount++;
    sessionCountElement.textContent = sessionCount;

    // After 4 pomodoros, take a long break
    if (sessionCount % 4 === 0) {
      switchMode("long-break");
    } else {
      switchMode("short-break");
    }

    if (settings.autoStartBreaks) {
      startTimer();
    }
  } else {
    switchMode("pomodoro");
    if (settings.autoStartPomodoros) {
      startTimer();
    }
  }

  startButton.disabled = false;
  pauseButton.disabled = true;
}

function setTimerForMode(mode) {
  switch (mode) {
    case "pomodoro":
      minutes = settings.pomodoroTime;
      document.body.className = "pomodoro-mode";
      break;
    case "short-break":
      minutes = settings.shortBreakTime;
      document.body.className = "short-break-mode";
      break;
    case "long-break":
      minutes = settings.longBreakTime;
      document.body.className = "long-break-mode";
      break;
  }
  seconds = 0;
  currentMode = mode;
}

function switchMode(mode) {
  clearInterval(timerInterval);
  isRunning = false;
  setTimerForMode(mode);
  updateTimerDisplay();

  // Update active button
  pomodoroButton.classList.remove("active");
  shortBreakButton.classList.remove("active");
  longBreakButton.classList.remove("active");

  switch (mode) {
    case "pomodoro":
      pomodoroButton.classList.add("active");
      break;
    case "short-break":
      shortBreakButton.classList.add("active");
      break;
    case "long-break":
      longBreakButton.classList.add("active");
      break;
  }

  updateDocumentTitle();
}

// Settings functionality
function toggleSettingsPanel() {
  settingsPanel.classList.toggle("hidden");
}

function saveSettings() {
  settings.pomodoroTime =
    parseInt(document.getElementById("pomodoro-time").value) || 25;
  settings.shortBreakTime =
    parseInt(document.getElementById("short-break-time").value) || 5;
  settings.longBreakTime =
    parseInt(document.getElementById("long-break-time").value) || 15;
  settings.autoStartBreaks =
    document.getElementById("auto-start-breaks").checked;
  settings.autoStartPomodoros = document.getElementById(
    "auto-start-pomodoros"
  ).checked;

  resetTimer();
  settingsPanel.classList.add("hidden");

  // Save to localStorage
  localStorage.setItem("pomodoroSettings", JSON.stringify(settings));
}

// Load settings from localStorage
function loadSettings() {
  const savedSettings = localStorage.getItem("pomodoroSettings");
  if (savedSettings) {
    settings = JSON.parse(savedSettings);

    document.getElementById("pomodoro-time").value = settings.pomodoroTime;
    document.getElementById("short-break-time").value = settings.shortBreakTime;
    document.getElementById("long-break-time").value = settings.longBreakTime;
    document.getElementById("auto-start-breaks").checked =
      settings.autoStartBreaks;
    document.getElementById("auto-start-pomodoros").checked =
      settings.autoStartPomodoros;
  }
}

// Event listeners
startButton.addEventListener("click", startTimer);
pauseButton.addEventListener("click", pauseTimer);
resetButton.addEventListener("click", resetTimer);
pomodoroButton.addEventListener("click", () => switchMode("pomodoro"));
shortBreakButton.addEventListener("click", () => switchMode("short-break"));
longBreakButton.addEventListener("click", () => switchMode("long-break"));
settingsButton.addEventListener("click", toggleSettingsPanel);
saveSettingsButton.addEventListener("click", saveSettings);

// Initialize
loadSettings();
setTimerForMode("pomodoro");
updateTimerDisplay();
updateDocumentTitle();

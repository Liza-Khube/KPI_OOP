const { app, BrowserWindow, Menu } = require("electron/main");
const path = require("node:path");

const createWindow = () => {
  const mainWin = new BrowserWindow({
    width: 1000,
    height: 600,
  });

  mainWin.loadFile(path.join(__dirname, "index.html"));
};

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

const menu = [
  {
    label: "File",
    submenu: [{ label: "Exit", role: "quit" }],
  },
  {
    label: "Actions",
    submenu: [{ label: "Work 1" }, { label: "Work 2" }],
  },
  {
    label: "Help",
    submenu: [{ label: "About", role: "about" }],
  },
];

Menu.setApplicationMenu(Menu.buildFromTemplate(menu));

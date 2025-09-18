const { app, BrowserWindow, Menu } = require("electron/main");
const path = require("node:path");
const { textField } = require("./module1");

let mainWin;

const createWindow = () => {
  mainWin = new BrowserWindow({
    width: 1000,
    height: 600,
    minWidth: 300,
    minHeight: 300,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  mainWin.loadFile(path.join(__dirname, "index.html"));

  mainWin.on("closed", () => {
    mainWin = null;
  });

  mainWin.webContents.openDevTools();
};

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

const menu = [
  {
    label: "File",
    submenu: [{ label: "Exit", role: "quit" }],
  },
  {
    label: "Actions",
    submenu: [
      {
        label: "Work 1",
        click: () => {
          textField(mainWin);
        },
      },
      { label: "Work 2" },
    ],
  },
  {
    label: "Help",
    submenu: [{ label: "About", role: "about" }],
  },
];
Menu.setApplicationMenu(Menu.buildFromTemplate(menu));

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

const { ipcMain, BrowserWindow } = require("electron");
const path = require("path");

const numSlider = (window) => {
  return new Promise((resolve) => {
    const modal = new BrowserWindow({
      width: 600,
      height: 250,
      parent: window,
      modal: true,
      resizable: false,
      autoHideMenuBar: true,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
      },
    });
    modal.loadFile(path.join(__dirname, "module2.html"));
    modal.once("ready-to-show", () => modal.show());

    const onValue = (event, value) => {
      ipcMain.removeListener("slider-canceled", onCancel);
      resolve(value);
      if (!modal.isDestroyed()) modal.close();
    };

    const onCancel = () => {
      ipcMain.removeListener("slider-value-selected", onValue);
      resolve(null);
      if (!modal.isDestroyed()) modal.close();
    };

    ipcMain.once("slider-value-selected", onValue);
    ipcMain.once("slider-canceled", onCancel);
  });
};

module.exports = { numSlider };

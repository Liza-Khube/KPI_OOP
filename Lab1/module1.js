const prompt = require("electron-prompt");

const textField = (window) => {
  return prompt({
    width: 500,
    height: 250,
    title: "Text field",
    label: "Enter your text",
    value: "text",
    inputAttrs: {
      type: "text",
    },
    type: "input",
  })
    .then((userText) => {
      if (userText !== null) {
        window.webContents.send("userText", userText);
      }
    })
    .catch(console.error);
};

module.exports = { textField };

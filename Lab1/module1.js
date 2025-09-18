const prompt = require("electron-prompt");

const textField = (window) => {
  return prompt({
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

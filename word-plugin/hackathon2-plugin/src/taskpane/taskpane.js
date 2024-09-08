Office.onReady(function () {
  // Office is ready
});

function insertText() {
  Word.run(function (context) {
    const doc = context.document;
    doc.body.insertText("Hello from the Word Add-in!", Word.InsertLocation.end);
    return context.sync();
  }).catch(function (error) {
    console.log("Error: " + error);
    if (error instanceof OfficeExtension.Error) {
      console.log("Debug info: " + JSON.stringify(error.debugInfo));
    }
  });
}

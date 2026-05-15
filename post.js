function doPost(e) {
  try {
    const sheet = SpreadsheetApp
      .openById('1iDg0gwUsS921vqEwH8aABv0XVIvgAg9dtIGUN0JoeEM')
      .getSheetByName('Sheet1');

    // Get all sheet data
    const data = sheet.getDataRange().getValues();

    // First row = headers
    const headers = data[0];

    // Query params (?id=123&email=test@test.com)
    const query = e.parameter;

    // JSON body
    const body = JSON.parse(e.postData.contents);

    // Find matching row
    let matchedRowIndex = -1;

    for (let i = 1; i < data.length; i++) {
      let row = data[i];
      let isMatch = true;

      for (let key in query) {
        const columnIndex = headers.indexOf(key);

        if (columnIndex === -1) {
          isMatch = false;
          break;
        }

        if (String(row[columnIndex]) !== String(query[key])) {
          isMatch = false;
          break;
        }
      }

      if (isMatch) {
        matchedRowIndex = i + 1; // Spreadsheet rows are 1-indexed
        break;
      }
    }

    // No row found
    if (matchedRowIndex === -1) {
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          message: 'No matching row found'
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // Update only provided fields
    for (let key in body) {
      const columnIndex = headers.indexOf(key);

      if (columnIndex !== -1) {
        sheet.getRange(matchedRowIndex, columnIndex + 1)
          .setValue(body[key]);
      }
    }

    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        updatedRow: matchedRowIndex
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: err.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

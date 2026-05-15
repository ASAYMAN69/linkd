function doGet(e) {
  // Open spreadsheet
  const sheet = SpreadsheetApp
    .openById('1iDg0gwUsS921vqEwH8aABv0XVIvgAg9dtIGUN0JoeEM')
    .getSheetByName('Sheet1');

  // Get all data
  const data = sheet.getDataRange().getValues();

  // First row = headers
  const headers = data[0];

  // Remaining rows
  const rows = data.slice(1);

  // Convert rows into objects
  const result = rows.map(row => {
    let obj = {};

    headers.forEach((header, index) => {
      obj[header] = row[index];
    });

    return obj;
  });

  // Return JSON
  return ContentService
    .createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}

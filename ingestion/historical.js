const readline = require("readline");
const { NseIndia } = require("stock-nse-india");
const { Parser } = require("json2csv");
const fs = require("fs");
const path = require("path");

const nseIndia = new NseIndia();

// Setup readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// Ask for user input
rl.question("Enter the NSE stock symbol (e.g., INFY, TCS, IRCTC): ", async (symbol) => {
  const startDate = new Date("2024-01-01");
  const endDate = new Date("2024-05-05");

  console.log(`Fetching data for ${symbol.toUpperCase()}...`);

  try {
    // Fetch data from the NSE India API
    const data = await nseIndia.getEquityHistoricalData(symbol.toUpperCase(), {
      start: startDate,
      end: endDate,
    });

    // Log the raw data to inspect the structure
    console.log("Raw Data:", JSON.stringify(data, null, 2));

    if (!data || data.length === 0) {
      console.log("No data found for the given symbol or date range.");
      rl.close();
      return;
    }

    // Check the structure of the first data entry
    console.log("First Data Entry:", data[0]);

    const parser = new Parser();
    const csv = parser.parse(data);

    const filename = path.join(__dirname, '..', 'data', `${symbol.toUpperCase()}_historical_data.csv`);

    // Save the CSV to the current directory
    fs.writeFileSync(filename, csv);
    console.log(`✅ Historical data saved to ${filename}`);
  } catch (error) {
    console.error("❌ Error fetching or saving data:", error.message);
  }

  rl.close();
});

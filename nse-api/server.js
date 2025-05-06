const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { NseIndia } = require('stock-nse-india');
const { Parser } = require('json2csv');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

const nseIndia = new NseIndia();

// Health check
app.get('/', (req, res) => {
  res.send('✅ NSE API Server is running');
});

// Historical data route: GET /historical/:symbol
app.get('/historical/:symbol', async (req, res) => {
  const { symbol } = req.params;
  const startDate = new Date('2024-01-01');
  const endDate = new Date('2024-05-05');

  try {
    const data = await nseIndia.getEquityHistoricalData(symbol.toUpperCase(), {
      start: startDate,
      end: endDate,
    });

    if (!data || data.length === 0) {
      return res.status(404).send('❌ No data found for this symbol or date range.');
    }

    // Convert JSON to CSV
    const parser = new Parser();
    const csv = parser.parse(data);

    // Save to ../data folder (outside nse-api folder)
    const dataFolderPath = path.join(__dirname, '..', 'data');
    const filename = `${symbol.toUpperCase()}_historical_data.csv`;
    const filePath = path.join(dataFolderPath, filename);

    if (!fs.existsSync(dataFolderPath)) {
      fs.mkdirSync(dataFolderPath, { recursive: true });
    }

    fs.writeFileSync(filePath, csv);

    // Respond with success and download link
    return res.status(200).json({
      message: '✅ Data fetched and saved as CSV successfully!',
      downloadLink: `/download/${filename}`,
    });

  } catch (error) {
    return res.status(500).send(`❌ Error fetching data: ${error.message}`);
  }
});

// Serve the saved CSV file via a download route
app.get('/download/:filename', (req, res) => {
  const { filename } = req.params;
  const filePath = path.join(__dirname, '..', 'data', filename);

  if (fs.existsSync(filePath)) {
    res.download(filePath);
  } else {
    res.status(404).send('❌ File not found');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`🚀 Server running on http://localhost:${port}`);
});

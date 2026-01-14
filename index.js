const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const app = express();

app.set('json spaces', 2);

const COPYRIGHT_STRING = "@AKASHHACKER";

async function getVehicleDetails(rcNumber) {
    const rc = rcNumber.trim().toUpperCase();
    const url = `https://vahanx.in/rc-search/${rc}`;

    const headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://vahanx.in/rc-search",
        "Accept-Language": "en-US,en;q=0.9"
    };

    try {
        const { data } = await axios.get(url, { headers, timeout: 10000 });
        const $ = cheerio.load(data);
        
        const details = {};
        
        // Helper function to find data by label
        const getValue = (label) => {
            const span = $(`span:contains("${label}")`);
            if (span.length > 0) {
                return span.parent().find('p').text().trim() || "N/A";
            }
            return "N/A";
        };

        const fields = [
            "Owner Name", "Father's Name", "Owner Serial No", "Model Name", "Maker Model",
            "Vehicle Class", "Fuel Type", "Fuel Norms", "Registration Date", "Insurance Company",
            "Insurance No", "Insurance Expiry", "Insurance Upto", "Fitness Upto", "Tax Upto",
            "PUC No", "PUC Upto", "Financier Name", "Registered RTO", "Address", "City Name", "Phone"
        ];

        fields.forEach(field => {
            details[field] = getValue(field);
        });

        return details;
    } catch (error) {
        return { error: "Vehicle Not Found or Website Down" };
    }
}

// Routes
app.get('/', (req, res) => {
    res.json({
        message: "🚗 Vehicle Search API by @AKASHHACKER is Live!",
        usage: "/lookup?rc=UP32XX1234",
        developer: COPYRIGHT_STRING
    });
});

app.get('/lookup', async (req, res) => {
    const rc = req.query.rc;
    if (!rc) {
        return res.status(400).json({ error: "Please provide ?rc= parameter", developer: COPYRIGHT_STRING });
    }

    const vehicleData = await getVehicleDetails(rc);

    if (vehicleData.error) {
        return res.status(404).json({ status: "error", message: vehicleData.error, developer: COPYRIGHT_STRING });
    }

    res.json({
        status: "success",
        ...vehicleData,
        copyright: COPYRIGHT_STRING
    });
});

module.exports = app;

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

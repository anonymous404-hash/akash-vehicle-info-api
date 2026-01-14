const express = require('express');
const axios = require('axios');
const app = express();

app.get('/', async (req, res) => {
    const rcNumber = req.query.rc_number;

    if (!rcNumber) {
        return res.status(400).json({
            "status": "error",
            "message": "Please provide an rc_number.",
            "credit": "API DEVELOPER: @AKASHHACKER"
        });
    }

    try {
        // Abhi-r API theke data fetch kora hochhe
        const response = await axios.get(`https://vehicle-info-api-abhi.vercel.app/?rc_number=${rcNumber}`);
        const apiData = response.data;

        // Ekhane amra response-ta sajachhi apnar name
        const myResponse = {
            "credit": "API DEVELOPER: @AKASHHACKER", // Ekhon apnar naam asbe
            "details": apiData.details || {},
            "rc_number": rcNumber.toUpperCase(),
            "status": apiData.status || "success"
        };

        res.json(myResponse);

    } catch (error) {
        res.status(500).json({
            "status": "error",
            "message": "Data fetch korte somossya hochhe ba RC bhul.",
            "credit": "API DEVELOPER: @AKASHHACKER"
        });
    }
});

module.exports = app;
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

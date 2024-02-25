const express = require('express');
const cors = require('cors');
const database = require("./database");
const path = require('path');
const app = express();

const port = process.env.port || 3000;
const axios = require('axios');

app.use(cors());
app.use(express.json());

app.use(express.static(path.join(__dirname, "browser")))

app.use(database.connectToMongoDB);
app.get("/allDetails", async (req, res) => {
    try {
        const collection = req.database.collection("pc_details");
        const allDetails = await collection.find().toArray()
        if (allDetails) {
            res.send({ success: true, details: allDetails });
        } else {
            res.send({ success: false, info: "No details" })
        }
    } catch (error) {
        res.status(500).send("Internal Server Error")
    }
});

app.post("/terminate", async (req, res) => {
    const pid = req.body.pid;
    const api_url = req.body.api_url;
    
    if (pid!= null) {
        try {
            const flaskResponse = await axios.post(api_url+'api/terminate', {pid: pid});
            res.send(flaskResponse.data)
        } catch (error) {   
            console.error('Error:', error.message);
            res.status(500).send('Error sending request to Flask server');
        }
    }
})

app.post("/refresh", async (req, res) => {
    const api_url = req.body.api_url;
    try {
        const flaskResponse = await axios.get(api_url+'api/refresh');
        res.send(flaskResponse.data)
    } catch (error) { 
        console.error('Error:', error.message);
        res.status(500).send('Error sending request to Flask server');
    }
   
})

app.get("*", async (req, res) => {
    res.sendFile(path.join(__dirname, "browser"))
})
app.use(database.closeMongoDB)
app.listen(port, () => {
    console.log("App is running at port " + port)
})
const express = require('express');
const fs = require('fs');
const app = express();
const port = 3000;


// TODO: CHECK AND KEEP/REMOVE:

// Enable CORS for all routes
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});



app.get('/api/courses/:courseId', (req, res) => {
    const courseId = req.params.courseId.toUpperCase();

    // Read data from the JSON file (replace with your actual file structure)
    const filePath = `courses/20241_${courseId}H5S_LEC0101.json`;

    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }

        try {
            const courseData = JSON.parse(data);
            res.json(courseData);
        } catch (parseError) {
            res.status(500).json({ error: 'Error parsing JSON file' });
        }
    });
});

app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`);
});

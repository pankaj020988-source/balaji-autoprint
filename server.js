const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json({ limit: '50mb' })); // मोठ्या फाईल्ससाठी लिमिट
app.use(express.static('public'));

let printQueue = [];

// मोबाईलवरून आलेला डेटा जसा आहे तसा स्वीकारणे
app.post('/upload-print', (req, res) => {
    try {
        printQueue.push(req.body);
        console.log('नवीन प्रिंट जॉब जमा झाला!');
        res.status(200).json({ success: true });
    } catch (error) {
        res.status(500).json({ error: 'एरर' });
    }
});

// कॉम्प्युटरसाठी डेटा देणे
app.get('/get-next-print', (req, res) => {
    if (printQueue.length > 0) {
        res.status(200).json(printQueue.shift());
    } else {
        res.status(200).json({ no_print: true });
    }
});

app.listen(PORT, () => {
    console.log(`सुरू झाला!`);
});

const express = require('express');
const multer = require('multer');
const path = require('path');
const app = express();

// ऑनलाईन सर्व्हरवर फाईल तात्पुरती सेव्ह करण्यासाठी
const storage = multer.diskStorage({
    destination: 'uploads/',
    filename: (req, file, cb) => cb(null, Date.now() + path.extname(file.originalname))
});
const upload = multer({ storage: storage });

let pendingPrints = []; // प्रिंट क्यू (Queue)

app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

// १. ग्राहकाने मोबाईलवरून फाईल अपलोड केल्यावर
app.post('/upload-print', upload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).send('फाईल मिळाली नाही.');
    
    const printJob = {
        id: Date.now(),
        fileUrl: `${req.protocol}://${req.get('host')}/uploads/${req.file.filename}`
    };
    pendingPrints.push(printJob); // क्यूमध्ये जॉब जोडला
    res.send('तुमची प्रिंट क्यूमध्ये जमा झाली आहे! थँक्यू!');
});

// २. दुकानाचा कॉम्प्युटर नवीन फाईल्स तपासण्यासाठी या लिंकवर येईल
app.get('/get-next-print', (req, res) => {
    if (pendingPrints.length > 0) {
        const nextJob = pendingPrints.shift(); // सर्वात पहिली प्रिंट बाहेर काढणे
        res.json(nextJob);
    } else {
        res.json({ no_print: true });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`ऑनलाईन सर्व्हर पोर्ट ${PORT} वर सुरू झाला आहे!`));
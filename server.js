const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// फाईल्स साठवण्यासाठी स्टोरेज सेटिंग
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'public/uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

// प्रिंट क्यू (Queue) साठवण्यासाठी लिस्ट
let printQueue = [];

// मोबाईलवरून येणारा डेटा स्वीकारणारा एंडपॉइंट (नवीन ऑप्शन्ससह)
app.post('/upload-print', upload.fields([{ name: 'file', maxCount: 1 }, { name: 'fileBack', maxCount: 1 }]), (req, res) => {
    try {
        const { printMode, jobType, bothSide } = req.body;
        
        if (!req.files || !req.files['file']) {
            return res.status(400).json({ error: 'फाईल मिळालेली नाही!' });
        }

        const mainFile = req.files['file'][0];
        const fileUrl = `${req.protocol}://${req.get('host')}/uploads/${mainFile.filename}`;
        
        let printJob = {
            id: Date.now(),
            fileUrl: fileUrl,
            printMode: printMode || 'color',
            jobType: jobType || 'normal',
            bothSide: bothSide === 'true',
            timestamp: new Date()
        };

        // जर आयडी कार्ड मोड असेल आणि दुसरी फाईल (मागचा भाग) आली असेल
        if (jobType === 'id_card' && req.files['fileBack']) {
            const backFile = req.files['fileBack'][0];
            printJob.fileUrlBack = `${req.protocol}://${req.get('host')}/uploads/${backFile.filename}`;
        }

        printQueue.push(printJob);
        console.log('नवीन प्रिंट जॉब जमा झाला:', printJob);
        
        res.status(200).json({ success: true, message: 'क्यूमध्ये जमा झाले!' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'सर्व्हर एरर!' });
    }
});

// कॉम्प्युटरमधील client.py साठी नवीन प्रिंट जॉब देणारा एंडपॉइंट
app.get('/get-next-print', (req, res) => {
    if (printQueue.length > 0) {
        const nextJob = printQueue.shift(); // पहिली फाईल बाहेर काढणे
        res.status(200).json(nextJob);
    } else {
        res.status(200).json({ no_print: true });
    }
});

// uploads फोल्डर तयार आहे ना हे तपासणे
const fs = require('fs');
if (!fs.existsSync('public/uploads')){
    fs.mkdirSync('public/uploads', { recursive: true });
}

app.listen(PORT, () => {
    console.log(`सर्व्हर पोर्ट ${PORT} वर सुरू झाला आहे...`);
});

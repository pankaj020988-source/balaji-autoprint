const express = require('express');
const multer = require('multer');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// फाईल्स थेट मेमरीमध्ये (RAM) साठवणे, जेणेकरून फोल्डर एरर येणार नाही
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

let printQueue = [];

// मोबाईलवरून येणारा डेटा स्वीकारणारा मुख्य एंडपॉइंट
app.post('/upload-print', upload.fields([{ name: 'file', maxCount: 1 }, { name: 'fileBack', maxCount: 1 }]), (req, res) => {
    try {
        if (!req.files || !req.files['file']) {
            return res.status(400).json({ error: 'फाईल मिळालेली नाही!' });
        }

        const { printMode, jobType, bothSide } = req.body;
        const mainFile = req.files['file'][0];
        
        // फाईलला Base64 डेटा फॉर्मेटमध्ये बदलणे जेणेकरून ती थेट ट्रान्सफर होईल
        const fileDataUri = `data:${mainFile.mimetype};base64,${mainFile.buffer.toString('base64')}`;
        
        let printJob = {
            id: Date.now(),
            fileUrl: fileDataUri, // थेट फाईलचा डेटा पाठवणे
            printMode: printMode || 'color',
            jobType: jobType || 'normal',
            bothSide: bothSide === 'true',
            timestamp: new Date()
        };

        if (jobType === 'id_card' && req.files['fileBack']) {
            const backFile = req.files['fileBack'][0];
            const backDataUri = `data:${backFile.mimetype};base64,${backFile.buffer.toString('base64')}`;
            printJob.fileUrlBack = backDataUri;
        }

        printQueue.push(printJob);
        console.log('नवीन प्रिंट जॉब क्यूमध्ये जमा झाला!');
        
        res.status(200).json({ success: true });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'सर्व्हर एरर!' });
    }
});

app.get('/get-next-print', (req, res) => {
    if (printQueue.length > 0) {
        res.status(200).json(printQueue.shift());
    } else {
        res.status(200).json({ no_print: true });
    }
});

app.listen(PORT, () => {
    console.log(`सर्व्हर पोर्ट ${PORT} वर यशस्वी सुरू झाला!`);
});

// routes/subscribers.js
const express = require('express');
const router = express.Router();
const Subscriber = require('../models/Subscriber');

router.post('/register', async (req, res) => {
  const { email } = req.body;
  try {
    const newSubscriber = new Subscriber({ email });
    await newSubscriber.save();
    res.status(201).json({ message: 'Email registered successfully' });
  } catch (error) {
    console.error(error); // エラー詳細をログに出力
    res.status(500).json({ message: 'Error registering email', error: error.message });
  }
});


module.exports = router;

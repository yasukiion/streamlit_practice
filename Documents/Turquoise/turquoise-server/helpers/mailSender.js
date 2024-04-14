// helpers/mailSender.js
const nodemailer = require('nodemailer');
const Subscriber = require('../models/Subscriber');

exports.sendDailyEmail = async function() {
  const subscribers = await Subscriber.find({});

  // Nodemailerの設定
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.GMAIL_USER,
      pass: process.env.GMAIL_PASSWORD
    }
  });

  // 各購読者にメールを送信
  subscribers.forEach(subscriber => {
    const mailOptions = {
      from: 'bluethebluest10001101001@gmail.com',
      to: subscriber.email,
      subject: 'Daily Research Papers',
      text: 'Here are your daily interesting research papers!'
    };

    transporter.sendMail(mailOptions, function(error, info) {
      if (error) {
        console.log('Error sending email:', error);
      } else {
        console.log('Email sent:', info.response);
      }
    });
  });
}

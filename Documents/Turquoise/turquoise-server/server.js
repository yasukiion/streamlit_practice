const express = require('express');
const mongoose = require('mongoose');
const subscriberRoutes = require('./routes/subscribers');
const cron = require('node-cron');
const { sendDailyEmail } = require('./helpers/mailSender');

const app = express();
app.use(express.json());

// MongoDBへの接続
mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log(err));

// サブスクライバールートへのルーティング
app.use('/api/subscribers', subscriberRoutes);

// ポートの設定とサーバーの起動
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// 毎朝8時にメールを送信
cron.schedule('0 8 * * *', () => {
  console.log('Running a task every day at 8 AM');
  sendDailyEmail();
});


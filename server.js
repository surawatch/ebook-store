const express = require('express');
const session = require('express-session');

const app = express();
const reportsRoutes = require('./routes/reports');
const authRoutes = require('./routes/auth');
const adminRoutes = require('./routes/admin');
const shopRoutes = require('./routes/shop');

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(session({
  secret: 'ebook-store-full-key-2026',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 24 * 60 * 60 * 1000 }
}));

app.use('/', authRoutes);

app.use('/', shopRoutes);

app.use('/admin', adminRoutes);

app.use('/reports', reportsRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
module.exports = app;
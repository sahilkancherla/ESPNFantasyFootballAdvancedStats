const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

require('dotenv').config()

mongoose.connect(process.env.MONGO_CLIENT_URL, {dbName: 'ESPNFFAdvancedStats'});
const database = mongoose.connection;
database.on('error', (error) => {
  console.log(error);
});
database.once('connected', () => {
  console.log('Database Connected');
});

const app = express();

// Add CORS middleware to allow requests from all origins
const corsOptions ={
    origin:'*', 
    credentials:true,            //access-control-allow-credentials:true
    optionSuccessStatus:200,
    allowedHeaders: 'Content-Type'
}

app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: false })); // Middleware to parse URL-encoded bodies

// Routes
app.use('/api/fantasyPlayerData', require('./routes/fantasyPlayerData'));

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

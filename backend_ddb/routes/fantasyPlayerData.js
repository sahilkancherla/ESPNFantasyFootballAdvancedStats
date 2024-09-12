const express = require('express');
const mongoose = require('mongoose');

const database = mongoose.connection;
const router = express.Router();


router.get('/', async (req, res) => {
  try {
    const { leagueId} = req.query;

    if (!leagueId) {
        return res.status(400).json({ message: 'Missing query parameter: leagueId' });
    }

    const fantasyPlayerCollection = database.collection('FantasyPlayerData');
    const nflPlayerCollection = database.collection('NFLPlayerData');

    const fantasyData = await fantasyPlayerCollection.find({ leagueId: leagueId.toString() }).toArray();
    const nflDataArray = await nflPlayerCollection.find().toArray();

    const nflData = nflDataArray.reduce((dict, player) => {
      dict[player.playerId] = player;
      return dict;
    }, {});

    res.json({
      nflData: nflData,
      fantasyData: fantasyData
    });

    
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;

'use client';

import { useState, useEffect } from 'react';
import { Title } from '@mantine/core';
import dotenv from 'dotenv';
import { Widget } from '../components/Widget/Widget';
import { LeagueMedianChart } from '../components/LeagueMedianChart/LeagueMedianChart';
import { MissedPoints } from '../components/MissedPoints/MissedPoints';

import classes from './page.module.css';

// Load environment variables from .env file
dotenv.config();

export default function HomePage() {
  const [stats, setStats] = useState(null);
  const [storedStats, setStoredStats] = useState(null);

  async function fetchStats() {
    console.log('Getting stats');
    try {
      const response = await fetch('http://127.0.0.1:5000/api/getAdvancedStats', {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const statsResponse = await response.json();
      setStats(statsResponse); // Update the state with fetched stats
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }


  async function fetchStoredStats() {
    console.log('Getting stored stats');
    try {
      const leagueId = '27289017';

      // Build the URL with query parameters
      const url = new URL('http://127.0.0.1:5001/api/fantasyPlayerData');
      url.searchParams.append('leagueId', leagueId);

      // Send the request with query parameters
      const response = await fetch(url.toString(), {
        cache: 'no-store',
      });

      const statsResponse = await response.json();
      setStoredStats(statsResponse); // Update the state with fetched stats
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
  }

  // Fetch stats immediately and set up an interval to fetch every 30 seconds
  useEffect(() => {
    fetchStats(); // Initial call to fetch stats
    fetchStoredStats(); // Initial call to fetch stored stats
    const intervalId = setInterval(fetchStats, 30000); // Run fetchStats every 30 seconds

    // Cleanup the interval on component unmount
    return () => clearInterval(intervalId);
  }, []); // Empty dependency array means this effect runs once when the component mounts

  return (
    <div className={classes.container}>
      {
        stats != null && storedStats != null ?
          <div>
            <Title className={classes.title}>
                League Median Tracker
            </Title>
            <Title className={classes.sub_title}>
                JAIRE Goat
            </Title>
            <Widget title={"League Median Tracker"} subtitle={"Tracking the league median for the current week"} content={<LeagueMedianChart data={stats}></LeagueMedianChart>}/>
            <Widget title={"Missed Points"} subtitle={"Calculating the best possible lineup and total missed points"} content={<MissedPoints currentData={stats} storedData = {storedStats} ></MissedPoints>}/>
          </div> : <></>
      }
    </div>
  );
}

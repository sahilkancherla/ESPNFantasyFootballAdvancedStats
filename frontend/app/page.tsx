'use client';

import { useState, useEffect } from 'react';
import { Title, Loader, Text } from '@mantine/core';
import { Widget } from '../components/Widget/Widget';
import { LeagueMedianChart } from '../components/LeagueMedianChart/LeagueMedianChart';
import { MissedPoints } from '../components/MissedPoints/MissedPoints';
import { PlayerTierData } from '../components/PlayerTierData/PlayerTierData';

import classes from './page.module.css';

export default function HomePage() {
  const [stats, setStats] = useState(null);
  const [storedStats, setStoredStats] = useState(null);

  async function fetchStats() {
    console.log('Getting stats');
    try {
      // Define your parameters
      const leagueId = '27289017';
      const swid = '864C6648-6746-42D3-A0D2-C2041D50FADD';
      const espnS2 = 'AEBLZmYmFB%2Fd0Ksi1rwg319dLQz44knGpDd6fp%2FhupuoLyJjsBxoeddNy1oBEkoMXeyDJJ6zycwok0PbMERfnC%2F5ZLD7JctADtj%2Fp8j9vmQNZZJqVTc7c4ki6qsxsK001kxqHgHQk8rIOu1Or4Qv4%2FR1BTUWfpRlQyfbfzRa%2FiQWgsqr8B%2BSdmLU0jS%2BDia%2BgXJjO2sz8QhEOzwqAhrJhyEv0RHx6vGjPdM%2Bm3ifgH1eZGknJr2fEXtS5NBezG5lm7cgfnktlWgvOFSMYuoHkAmv9Urb2G7x8u19b8fuJplODA%3D%3D';
      const year = 2024;
      const week = 7;
      const leagueMedianName = 'League Median';
      const teamIdAgainstLeagueMedian = 6;

      // Construct the URL with query parameters

      const url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_API_URL}/api/getAdvancedStats`);
      url.searchParams.append('leagueId', leagueId);
      url.searchParams.append('swid', swid);
      url.searchParams.append('espnS2', espnS2);
      url.searchParams.append('year', year.toString());
      url.searchParams.append('week', week.toString());
      url.searchParams.append('leagueMedianName', leagueMedianName);
      url.searchParams.append('teamIdAgainstLeagueMedian', teamIdAgainstLeagueMedian.toString());

      // Make the fetch request
      const response = await fetch(url, {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Handle the response
      const data = await response.json();

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      setStats(data); // Update the state with fetched stats
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }

  async function fetchStoredStats() {
    console.log('Getting stored stats');
    try {
      const leagueId = '27289017';

      // Build the URL with query parameters
      const url = new URL(`${process.env.NEXT_PUBLIC_BACKEND_DDB_API_URL}/api/fantasyPlayerData`);
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
                ESPN Fantasy Football Advanced Stats
            </Title>
            <Title className={classes.sub_title}>
                League: JAIRE Goat
            </Title>
            <Widget title="League Median Tracker" subtitle="Tracking the league median for the current week" content={<LeagueMedianChart data={stats}></LeagueMedianChart>} />
            <Widget title="Missed Points" subtitle="Calculating the best possible lineup and total missed points" content={<MissedPoints currentData={stats} storedData={storedStats}></MissedPoints>} />
            <Widget title="Player Tiers" subtitle="Dividing the players into tiers" content={<PlayerTierData currentData={stats} storedData={storedStats}></PlayerTierData>} />

          </div> :
          <div className={classes.loading}>
            <Loader color="blue" />
            <Text className={classes.loadingText}>Fetching fantasy football advanced stats...</Text>
          </div>
      }
    </div>
  );
}

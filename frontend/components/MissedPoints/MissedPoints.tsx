/* eslint-disable max-len */
// @ts-nocheck

'use client';


import { Text, Badge, Card, Group, Accordion } from '@mantine/core';
import classes from './MissedPoints.module.css';

function UserDataCard({ item, nflPlayerData}) {

    const { actualLineup, betterLineup } = item;

    const starters = actualLineup.filter(player => player.slotPosition !== 'BE' && player.slotPosition !== 'IR');
    const startersSet = new Set(starters.map(player => player.playerId));

    betterLineup.forEach(player => {
      player.started = startersSet.has(player.id);
    });

    return (
        <div className={classes.container}>
            <p className={classes.actual_points}>
              Actual Points: {item.actualPoints}, Best Points: {item.betterPoints}
            </p>
            <p className={classes.missed_points}>
              {item.teamName} missed out on {item.missedPoints} points
            </p>

            <h3>Ideal Lineup</h3>
            <div className={classes.ideal_lineup_container}>
                {betterLineup.length > 0 ? (
                    betterLineup.map((player) => (

                      <Card shadow="sm" padding="lg" radius="md" withBorder className = {classes.player_started_container}>
                          <Group justify="space-between" mt="md" mb="xs">
                            <Text fw={500}>{nflPlayerData[player.id].name} ({player.slot})</Text>
                            <Badge color={player.started ? "green" : "red"}>{player.started ? "Started" : "Benched"}</Badge>
                          </Group>

                          <Text size="sm" c="dimmed">
                          {nflPlayerData[player.id].name} scored {player.points} points against {player.opponent} this week.
                          </Text>

                      </Card>
                    ))
                ) : (
                    <p>No players to show.</p>
                )}
            </div>
        </div>
    );
}

export function MissedPoints({ currentData, storedData }) {
    const currentWeek = 1;
 
    const {nflData, fantasyData} = storedData;

    function getMissedPointsArrayForWeek(week) {
      const currentWeekDataArray = [];
      fantasyData.forEach((teamData) => {
        const currentWeekDataForTeam = teamData.weekInformation[week];

        if (currentWeekDataForTeam.missedPoints != null) {
          currentWeekDataArray.push({
            id: teamData.teamId,
            teamName: teamData.teamName,
            actualPoints: currentWeekDataForTeam.score,
            betterPoints: currentWeekDataForTeam.missedPoints.bestPoints,
            missedPoints: (currentWeekDataForTeam.missedPoints.bestPoints - currentWeekDataForTeam.score).toFixed(2),
            betterLineup: currentWeekDataForTeam.missedPoints.bestLineup,
            actualLineup: currentWeekDataForTeam.lineup,
          });
        }
      });
      return currentWeekDataArray;
    }

    const currentWeekDataArray = getMissedPointsArrayForWeek(currentWeek.toString());

    const items = currentWeekDataArray.map((item) => (

      <div>
      {
        item.missedPoints ?
          <Accordion.Item key={item.id} value={item.teamName}>
            <Accordion.Control className={classes.accordion_control}>
              <Badge color="blue" className={classes.badge_spacing}>{item.missedPoints}</Badge>
              <span className={classes.preview_text}>{item.teamName}</span>
            </Accordion.Control>
            <Accordion.Panel>
              <UserDataCard item={item} nflPlayerData = {nflData}></UserDataCard>
            </Accordion.Panel>
          </Accordion.Item>
        : null
      }
      </div>
    ));

    return (
      <div className="wrapper">
          <Accordion defaultValue="1">
            {items}
          </Accordion>
      </div>
    );
}

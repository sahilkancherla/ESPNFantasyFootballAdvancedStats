/* eslint-disable max-len */

'use client';

import { useState } from 'react';
import { Text, SegmentedControl } from '@mantine/core';
import { BarChart } from '@mantine/charts';

import classes from './LeagueMedianChart.module.css';

const normalCurrentColor = 'blue.6';
const leagueMedianCurrentColor = 'red.6';
const againstLeagueMedianCurrentColor = 'green.6';
const CURRENT_TEXT = 'current';
const PROJECTED_TEXT = 'projected';

const LEAGUE_MEDIAN_ID = '100';
const LEAGUE_MEDIAN_NAME = 'League Median';


interface Scores {
    [key: string]: number;
}

interface ScoreEntry {
    teamId: string;
    teamName: string;
    currentScore: number;
    projectedScore: number;
    color: string,
}

interface Team {
    ownerId: String;
    teamName: String;
}

// Function to convert the data into an array of objects
const convertToArray = (idToTeam: Team[], currentScores: Scores, projectedScores: Scores,
    againstLeagueMedianId: String): ScoreEntry[] =>
        Object.keys(currentScores).map(id => ({
            teamId: id,
            teamName: idToTeam[id] ? idToTeam[id].teamName : 'League Median',
            currentScore: currentScores[id],
            projectedScore: projectedScores[id],
            color: id !== againstLeagueMedianId ? normalCurrentColor :
                againstLeagueMedianCurrentColor,
        }));

export function LeagueMedianChart({ data }) {
    const [currentView, setCurrentView] = useState(CURRENT_TEXT);

    const idToTeam = data.leagueData.teams;
    const { currentWeekScoresData, leagueMedianData } = data;
    const againstLeagueMedianId = leagueMedianData.teamIdAgainstLeagueMedian;
    const againstLeagueMedianTeamName = idToTeam[againstLeagueMedianId].teamName;
    const againstLeagueMedianTeamCurrentPoints =
        data.currentWeekScoresData.currentScores[againstLeagueMedianId];
    const againstLeagueMedianTeamProjectedPoints =
        data.currentWeekScoresData.projectedScores[againstLeagueMedianId];

    const currentDiffToLeagueMedian = againstLeagueMedianTeamCurrentPoints - leagueMedianData.currentMedian;
    const projectedDiffToLeagueMedian = againstLeagueMedianTeamProjectedPoints - leagueMedianData.projectedMedian;

    // Convert data
    const scoreEntries = convertToArray(idToTeam, currentWeekScoresData.currentScores, currentWeekScoresData.projectedScores, againstLeagueMedianId.toString());

    const leagueMedianScoreEntry = {
        teamId: LEAGUE_MEDIAN_ID,
        teamName: LEAGUE_MEDIAN_NAME,
        currentScore: leagueMedianData.currentMedian,
        projectedScore: leagueMedianData.projectedMedian,
        color: leagueMedianCurrentColor,
    };

    scoreEntries.push(leagueMedianScoreEntry);

    // Sort by currentScore
    const sortedByCurrentScore = [...scoreEntries].sort((a, b) => a.currentScore - b.currentScore);

    // Sort by projectedScore
    const sortedByProjectedScore = [...scoreEntries].sort((a, b) => a.projectedScore - b.projectedScore);

  return (
    <div>
        <SegmentedControl
          value={currentView}
          onChange={setCurrentView}
          color="blue"
          data={[
            { label: 'Current', value: CURRENT_TEXT },
            { label: 'Projected', value: PROJECTED_TEXT },
          ]}
          className={classes.segmentedControl}
        />
        {
          currentView === CURRENT_TEXT ?
                <div>
                    <div className={classes.container}>
                        <BarChart
                          h={300}
                          data={sortedByCurrentScore}
                          dataKey={"teamName"}
                          series={[
                                { name: 'currentScore', color: 'blue' },
                            ]}
                          tickLine="y"
                        />
                    </div>
                    <Text>The current league median is at {leagueMedianData.currentMedian}. {againstLeagueMedianTeamName} is {currentDiffToLeagueMedian > 0 ? 'ahead' : 'behind'} by {Math.abs(currentDiffToLeagueMedian).toFixed(2)} points.</Text>
                </div> :
                <div>
                    <div className={classes.container}>
                        <BarChart
                          h={300}
                          data={sortedByProjectedScore}
                          dataKey={"teamName"}
                          series={[
                                { name: 'projectedScore', color: 'blue' },
                            ]}
                          tickLine="y"
                        />
                    </div>
                    <Text>The projected league median is at {leagueMedianData.projectedMedian}. {againstLeagueMedianTeamName} is {projectedDiffToLeagueMedian > 0 ? 'ahead' : 'behind'} by {Math.abs(projectedDiffToLeagueMedian).toFixed(2)} points.</Text>
                </div>

        }
    </div>
  );
}

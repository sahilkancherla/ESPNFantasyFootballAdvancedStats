// @ts-nocheck

'use client';

import { Card, Text, Group, Badge, Menu, Button } from '@mantine/core';
import { useState } from 'react';
import classes from './PlayerTierData.module.css';


function TierRow({ label, playerIdsInTier, nflPlayerData}) {

    console.log("for " + label + " we have " + playerIdsInTier)

    for (const index in playerIdsInTier){
        console.log(playerIdsInTier[index])
        console.log(nflPlayerData[playerIdsInTier[index]])
    }


    const parts = label.split("_");

    const position = parts[0];
    const tier = Number(parts[1]);

    return (

        <div>
            <div className={classes.tierBanner}>
                {
                    tier === 1 ?
                    <div className={classes.tierBannerText}>
                        {position}
                    </div> :
                    <div></div>
                }
            </div>

            <div className={classes.row}>
                <div className={classes.box15}>
                    Tier {tier}
                </div>
                <div className={classes.box85}>
                    {playerIdsInTier ? (
                    playerIdsInTier.map((playerId) => (
                        nflPlayerData[playerId] ? (
                        <Card key={playerId} shadow="sm" padding="lg" radius="md" withBorder className={classes.player_started_container}>
                            <Group justify="space-between" mt="md" mb="xs">
                            <Text fw={500}>{nflPlayerData[playerId].name}</Text>
                            <Badge color="green">{nflPlayerData[playerId].primaryPosition} {nflPlayerData[playerId].positionRank}</Badge>
                            </Group>
                        </Card>
                        ) : null
                    ))
                    ) : (
                    <div className={classes.noPlayers}>
                        <Text>No players in this tier</Text>
                    </div>
                    )}
                </div>
            </div>
        </div>
      );
}


export function PlayerTierData({currentData, storedData}) {

    const {playerTierInformation} = currentData;
    const {nflData, fantasyData} = storedData;
    const [currentTeamId, setCurrentTeamId] = useState(1);


    const playerPositionsArray: string[] = [
        'QB_1', 'QB_2',
        'RB_1', 'RB_2', 'RB_3',
        'WR_1', 'WR_2', 'WR_3',
        'TE_1', 'TE_2',
        'D/ST_1', 'D/ST_2',
        'K_1', 'K_2',
      ];
    const playerPositionsSet: Set<string> = new Set(playerPositionsArray);

    return (
        <div className={classes.container}>

            <Text className={classes.currentTeam}>
                Currently viewing <span className={classes.teamName}>{fantasyData[currentTeamId-1].teamName}</span> tier breakdown
            </Text>
            <Menu shadow="md" className ={classes.menuButton}>
                <Menu.Target>
                    <Button>View another player</Button>
                </Menu.Target>

                <Menu.Dropdown>
                    <Menu.Label>Teams</Menu.Label>
                    {fantasyData.map((fantasyPlayer) => (
                        <Menu.Item
                            key={fantasyPlayer.teamId}
                            onClick={() => setCurrentTeamId(fantasyPlayer.teamId)}
                        >
                            {fantasyPlayer.teamName}
                        </Menu.Item>
                    ))}
                </Menu.Dropdown>
            </Menu>
            <div>
                {playerPositionsArray.map((position) => (
                    <TierRow
                        label={position}
                        playerIdsInTier={playerTierInformation[currentTeamId][position]}
                        nflPlayerData={nflData}
                    />
                ))}
            </div>
        </div>
    );
}

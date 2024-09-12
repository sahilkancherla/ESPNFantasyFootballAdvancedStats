// @ts-nocheck

import { Divider, Paper, Text, Title } from '@mantine/core';
import classes from './Widget.module.css';
import { LeagueMedianChart } from '../LeagueMedianChart/LeagueMedianChart';

export function Widget({title, subtitle, content}) {
  return (
    <div className={classes.container}>
        <Paper shadow="xs" p="xl">
            <Title className={classes.title}>{title}</Title>
            <Text>{subtitle}</Text>
            {content}
        </Paper>
    </div>
  );
}

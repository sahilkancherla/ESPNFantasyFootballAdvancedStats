// @ts-nocheck

import { useState } from 'react';
import { Paper, Title, Text, Collapse, Button, Divider} from '@mantine/core';
import { IconChevronUp, IconChevronDown } from '@tabler/icons-react';
import classes from './Widget.module.css';

export function Widget({ title, subtitle, content }) {
  const [opened, setOpened] = useState(true);

  return (
    <div className={classes.container}>
      <Paper shadow="xs" p="xl" withBorder>
        <div className={classes.header}>
          <div>
            <Title className={classes.title}>{title}</Title>
            <Text className={classes.subtitle}>{subtitle}</Text>
          </div>
          <Button
            variant="subtle"
            onClick={() => setOpened((prev) => !prev)}
            size="xs"
          >
            {opened ? <IconChevronUp size={16} /> : <IconChevronDown size={16} />}
          </Button>
        </div>
        <Divider my="md" />
        {
          !opened ? <div className={classes.closedContent}>Expand to see '{title}'</div> : <></>
        }
        <Collapse in={opened}>
          <div className={classes.content}>
            {content}
          </div>
        </Collapse>
      </Paper>
    </div>
  );
}

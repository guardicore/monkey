'use client';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import NumberedCard from '@/_components/getting-started/NumberedCard';
import Stack from '@mui/material/Stack';
import ConstructionIcon from '@mui/icons-material/Construction';
import SecurityIcon from '@mui/icons-material/Security';
import LanIcon from '@mui/icons-material/Lan';
import AssessmentIcon from '@mui/icons-material/Assessment';
import Divider from '@mui/material/Divider';

const GettingStarted = () => {
    return (
        <Card
            variant="outlined"
            sx={{
                background: '#ffcc0070',
                padding: '2em',
                borderRadius: '20px'
            }}>
            <Stack direction="column" spacing={2}>
                <Box>
                    <h2>How it works?</h2>
                    <p>
                        The Monkey uses various methods to propagate across a
                        data center and reports to this Monkey Island Control
                        server
                    </p>
                </Box>
                <Divider />
                <Stack direction="row" spacing={2}>
                    <NumberedCard number={1} title="First card">
                        <ConstructionIcon fontSize="large" />
                        <p>
                            <b>Setup your Malware</b>
                        </p>
                        <p>Configure what you want the malware to do</p>
                    </NumberedCard>
                    <NumberedCard number={2} title="Second card">
                        <SecurityIcon fontSize="large" />
                        <p>
                            <b>Run Monkey</b>
                        </p>
                        <p>Configure what you want the malware to do</p>
                    </NumberedCard>
                    <NumberedCard number={3} title="Second card">
                        <LanIcon fontSize="large" />
                        <p>
                            <b>Review Infection Map</b>
                        </p>
                        <p>Configure what you want the malware to do</p>
                    </NumberedCard>
                    <NumberedCard number={4} title="Second card">
                        <AssessmentIcon fontSize="large" />
                        <p>
                            <b>Security Reports</b>
                        </p>
                        <p>Configure what you want the malware to do</p>
                    </NumberedCard>
                </Stack>
            </Stack>
        </Card>
    );
};

export default GettingStarted;

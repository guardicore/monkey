import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import TabLabel from './TabLabel';
import CardActionArea from '@mui/material/CardActionArea';

export interface NumberedCardProps {
    children: React.ReactNode;
    number: number;
    icon?: React.ReactNode;
    title?: string;
}

const NumberedCard = (props: NumberedCardProps) => {
    return (
        <>
            <Box
                sx={{
                    display: 'inline-flex'
                }}>
                <TabLabel>{props.number}</TabLabel>
                <Card>
                    <CardActionArea>
                        <CardContent>{props.children}</CardContent>
                    </CardActionArea>
                </Card>
            </Box>
        </>
    );
};

export default NumberedCard;

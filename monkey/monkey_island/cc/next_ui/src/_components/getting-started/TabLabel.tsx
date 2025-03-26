import { styled } from '@mui/material/styles';

export interface NumberedTabProps {
    number: number;
    color?: string;
}

const NumberedTabSpan = styled('span')(({ theme }) => ({
    height: '24px',
    fontSize: '16px',
    paddingLeft: '7px',
    paddingRight: '3px',
    marginTop: '15px',
    textAlign: 'center',
    left: 0,
    top: '1em',
    borderRadius: '12px 0 0 12px',
    color: theme.palette.primary.contrastText,
    background: theme.palette.primary.main
}));

export default NumberedTabSpan;

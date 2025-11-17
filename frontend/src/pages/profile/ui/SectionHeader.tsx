import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import EditIcon from '@mui/icons-material/Edit';

interface SectionHeaderProps {
  title: string;
  subtitle: string;
  onEditClick: () => void;
}

export function SectionHeader({
  title,
  subtitle,
  onEditClick,
}: SectionHeaderProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        mb: 3,
      }}>
      <Box>
        <Typography variant='h6' component='h2' gutterBottom>
          {title}
        </Typography>
        <Typography variant='body2' color='text.secondary'>
          {subtitle}
        </Typography>
      </Box>
      <Button
        startIcon={<EditIcon />}
        variant='outlined'
        size='small'
        onClick={onEditClick}>
        Edit
      </Button>
    </Box>
  );
}

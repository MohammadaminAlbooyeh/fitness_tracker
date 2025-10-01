import { formatDistanceToNow, format } from 'date-fns';

export const formatDuration = (minutes) => {
  if (minutes < 60) {
    return `${minutes} min`;
  }
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return remainingMinutes > 0 
    ? `${hours}h ${remainingMinutes}m`
    : `${hours}h`;
};

export const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  return {
    date: format(date, 'MMM d, yyyy'),
    time: format(date, 'h:mm a'),
    relative: formatDistanceToNow(date, { addSuffix: true })
  };
};
import React from 'react';
import { Button, Typography, Container, Box } from '@mui/material';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <Container maxWidth="md" style={{ textAlign: 'center', marginTop: '2rem' }}>
      <Typography variant="h2" gutterBottom>
        Welcome to Fitness Tracker
      </Typography>
      <Typography variant="h6" gutterBottom>
        Track your workouts, monitor your progress, and achieve your fitness goals.
      </Typography>
      <Box mt={4}>
        <Button
          variant="contained"
          color="primary"
          size="large"
          component={Link}
          to="/register"
          style={{ marginRight: '1rem' }}
        >
          Get Started
        </Button>
        <Button
          variant="outlined"
          color="primary"
          size="large"
          component={Link}
          to="/login"
        >
          Login
        </Button>
      </Box>
    </Container>
  );
};

export default LandingPage;
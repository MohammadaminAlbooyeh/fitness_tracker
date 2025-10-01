import React from 'react';
import { Box, Container } from '@mui/material';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        height: '100vh',
        overflow: 'auto',
        pt: 3,
        pb: 3,
      }}
    >
      <Container maxWidth="lg">{children}</Container>
    </Box>
  );
};

export default MainLayout;
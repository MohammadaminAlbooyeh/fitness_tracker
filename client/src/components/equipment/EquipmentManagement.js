import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Tabs,
  Tab,
  Typography,
  Alert
} from '@mui/material';
import {
  Inventory as InventoryIcon,
  Build as MaintenanceIcon,
  Assessment as StatsIcon,
  QrCode as QRIcon
} from '@mui/icons-material';
import EquipmentInventory from './EquipmentInventory';
import MaintenanceManager from './MaintenanceManager';
import EquipmentStats from './EquipmentStats';
import QRScanner from './QRScanner';

const EquipmentManagement = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [alert, setAlert] = useState(null);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const showAlert = (message, severity = 'success') => {
    setAlert({ message, severity });
    setTimeout(() => setAlert(null), 5000);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {alert && (
        <Alert 
          severity={alert.severity}
          sx={{ mb: 2 }}
          onClose={() => setAlert(null)}
        >
          {alert.message}
        </Alert>
      )}

      <Paper sx={{ mb: 2 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="fullWidth"
          indicatorColor="primary"
          textColor="primary"
          aria-label="equipment management tabs"
        >
          <Tab
            icon={<InventoryIcon />}
            label="Inventory"
            iconPosition="start"
          />
          <Tab
            icon={<MaintenanceIcon />}
            label="Maintenance"
            iconPosition="start"
          />
          <Tab
            icon={<StatsIcon />}
            label="Statistics"
            iconPosition="start"
          />
          <Tab
            icon={<QRIcon />}
            label="QR Scanner"
            iconPosition="start"
          />
        </Tabs>
      </Paper>

      <Box sx={{ mt: 2 }}>
        {activeTab === 0 && (
          <EquipmentInventory onAlert={showAlert} />
        )}
        {activeTab === 1 && (
          <MaintenanceManager onAlert={showAlert} />
        )}
        {activeTab === 2 && (
          <EquipmentStats />
        )}
        {activeTab === 3 && (
          <QRScanner onAlert={showAlert} />
        )}
      </Box>
    </Container>
  );
};

export default EquipmentManagement;
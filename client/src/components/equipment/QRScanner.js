import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress
} from '@mui/material';
import { QrReader } from 'react-qr-reader';
import { useQuery } from 'react-query';
import { getEquipmentByQRCode } from '../../api/equipment';

const QRScanner = ({ onAlert }) => {
  const [scanning, setScanning] = useState(false);
  const [scannedData, setScannedData] = useState(null);

  const { data: equipment, isLoading } = useQuery(
    ['equipment', scannedData],
    () => scannedData ? getEquipmentByQRCode(scannedData) : null,
    {
      enabled: !!scannedData,
      onError: (error) => {
        onAlert(error.message, 'error');
        setScannedData(null);
      }
    }
  );

  const handleScan = (result) => {
    if (result) {
      setScanning(false);
      setScannedData(result.text);
    }
  };

  const handleError = (error) => {
    console.error(error);
    onAlert('Error accessing camera: ' + error.message, 'error');
    setScanning(false);
  };

  const handleStartScan = () => {
    setScanning(true);
    setScannedData(null);
  };

  const handleCloseScan = () => {
    setScanning(false);
  };

  return (
    <Box>
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          QR Code Scanner
        </Typography>
        <Typography color="textSecondary" paragraph>
          Scan equipment QR codes to quickly access information and record usage.
        </Typography>
        <Button
          variant="contained"
          onClick={handleStartScan}
          disabled={scanning}
        >
          {scanning ? 'Scanning...' : 'Start Scanning'}
        </Button>
      </Paper>

      {/* Scanner Dialog */}
      <Dialog
        open={scanning}
        onClose={handleCloseScan}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Scan Equipment QR Code</DialogTitle>
        <DialogContent>
          <Box sx={{ width: '100%', height: 300 }}>
            <QrReader
              onResult={handleScan}
              onError={handleError}
              constraints={{ facingMode: 'environment' }}
              style={{ width: '100%' }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseScan}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Equipment Details */}
      {scannedData && (
        <Paper sx={{ p: 2 }}>
          {isLoading ? (
            <Box display="flex" justifyContent="center" p={3}>
              <CircularProgress />
            </Box>
          ) : equipment ? (
            <Box>
              <Typography variant="h6" gutterBottom>
                {equipment.name}
              </Typography>
              <Typography color="textSecondary" paragraph>
                Category: {equipment.category.name}
              </Typography>
              <Typography paragraph>
                {equipment.description}
              </Typography>
              <Typography>
                Status: {equipment.status}
              </Typography>
              <Typography>
                Location: {equipment.location}
              </Typography>
              <Typography>
                Usage: {equipment.current_usage_hours}/{equipment.max_usage_hours} hours
              </Typography>
              
              <Box sx={{ mt: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => {/* Handle start usage */}}
                  disabled={equipment.status !== 'available'}
                >
                  Start Using Equipment
                </Button>
              </Box>
            </Box>
          ) : (
            <Typography color="error">
              Equipment not found
            </Typography>
          )}
        </Paper>
      )}
    </Box>
  );
};

export default QRScanner;
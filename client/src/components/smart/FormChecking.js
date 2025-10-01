import React, { useState, useRef } from 'react';
import {
  Container,
  Grid,
  Typography,
  Paper,
  Box,
  Button,
  CircularProgress,
  IconButton,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip
} from '@mui/material';
import {
  PhotoCamera as CameraIcon,
  Check as CheckIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Save as SaveIcon
} from '@mui/icons-material';
import { useQuery, useMutation } from 'react-query';
import { format } from 'date-fns';
import { 
  uploadFormCheckVideo,
  startFormCheck,
  getFormCheckResults,
  saveFormCheckFeedback
} from '../../api/smart_features';

const FormFeedback = ({ feedback }) => {
  const getFeedbackIcon = (severity) => {
    switch (severity) {
      case 'error':
        return <ErrorIcon color="error" />;
      case 'warning':
        return <WarningIcon color="warning" />;
      default:
        return <CheckIcon color="success" />;
    }
  };

  return (
    <List>
      {feedback.map((item, index) => (
        <ListItem key={index}>
          <ListItemIcon>
            {getFeedbackIcon(item.severity)}
          </ListItemIcon>
          <ListItemText
            primary={item.message}
            secondary={item.suggestion}
          />
        </ListItem>
      ))}
    </List>
  );
};

const FormAnalysis = ({ analysis }) => {
  return (
    <Grid container spacing={2}>
      {Object.entries(analysis).map(([metric, value]) => (
        <Grid item xs={12} sm={6} md={4} key={metric}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              {metric.split('_').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
              ).join(' ')}
            </Typography>
            <Box display="flex" alignItems="center">
              <LinearProgress
                variant="determinate"
                value={value}
                sx={{ flexGrow: 1, mr: 2 }}
              />
              <Typography variant="body2">
                {value}%
              </Typography>
            </Box>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
};

const FormChecking = () => {
  const [recording, setRecording] = useState(false);
  const [currentCheck, setCurrentCheck] = useState(null);
  const [selectedExercise, setSelectedExercise] = useState(null);
  const [viewResults, setViewResults] = useState(false);
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'video/webm' });
        const formData = new FormData();
        formData.append('video', blob);
        formData.append('exercise_id', selectedExercise.id);
        
        const response = await uploadFormCheckVideo(formData);
        setCurrentCheck(response.check_id);
        startFormCheckMutation.mutate(response.check_id);
      };

      mediaRecorderRef.current.start();
      setRecording(true);
    } catch (err) {
      console.error('Error accessing camera:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      setRecording(false);
    }
  };

  const startFormCheckMutation = useMutation(startFormCheck, {
    onSuccess: () => {
      // Start polling for results
      const pollInterval = setInterval(async () => {
        const results = await getFormCheckResults(currentCheck);
        if (results.status === 'completed') {
          clearInterval(pollInterval);
          setViewResults(true);
        }
      }, 2000);
    }
  });

  const { data: formCheckResults, isLoading: loadingResults } = useQuery(
    ['formCheckResults', currentCheck],
    () => getFormCheckResults(currentCheck),
    {
      enabled: !!currentCheck && viewResults,
      refetchInterval: (data) => 
        data?.status === 'completed' ? false : 2000
    }
  );

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h4" gutterBottom>
              AI Form Check
            </Typography>
          </Grid>

          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 3 }}>
              <Box 
                sx={{
                  position: 'relative',
                  width: '100%',
                  paddingTop: '56.25%' // 16:9 aspect ratio
                }}
              >
                <video
                  ref={videoRef}
                  autoPlay
                  muted
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    backgroundColor: '#000'
                  }}
                />
                {!selectedExercise ? (
                  <Box
                    sx={{
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      transform: 'translate(-50%, -50%)',
                      textAlign: 'center'
                    }}
                  >
                    <Typography variant="h6" gutterBottom>
                      Select an exercise to begin
                    </Typography>
                    <Button
                      variant="contained"
                      onClick={() => setSelectedExercise({ id: 1, name: 'Squat' })}
                    >
                      Choose Exercise
                    </Button>
                  </Box>
                ) : recording ? (
                  <IconButton
                    sx={{
                      position: 'absolute',
                      bottom: 16,
                      left: '50%',
                      transform: 'translateX(-50%)',
                      backgroundColor: 'error.main',
                      '&:hover': {
                        backgroundColor: 'error.dark'
                      }
                    }}
                    onClick={stopRecording}
                  >
                    <StopIcon />
                  </IconButton>
                ) : (
                  <IconButton
                    sx={{
                      position: 'absolute',
                      bottom: 16,
                      left: '50%',
                      transform: 'translateX(-50%)',
                      backgroundColor: 'success.main',
                      '&:hover': {
                        backgroundColor: 'success.dark'
                      }
                    }}
                    onClick={startRecording}
                  >
                    <PlayIcon />
                  </IconButton>
                )}
              </Box>

              {selectedExercise && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="h6">
                    {selectedExercise.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Record yourself performing the exercise to get AI feedback
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>

          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Instructions
              </Typography>
              <List>
                <ListItem>
                  <ListItemText
                    primary="1. Select an exercise"
                    secondary="Choose the exercise you want to analyze"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="2. Position yourself"
                    secondary="Ensure your full body is visible in the frame"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="3. Record your set"
                    secondary="Perform 3-5 repetitions of the exercise"
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="4. Get AI feedback"
                    secondary="Receive detailed analysis and suggestions"
                  />
                </ListItem>
              </List>
            </Paper>
          </Grid>
        </Grid>

        {/* Results Dialog */}
        <Dialog
          open={viewResults && formCheckResults?.status === 'completed'}
          onClose={() => setViewResults(false)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle>Form Check Results</DialogTitle>
          <DialogContent>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={3}>
                  <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Overall Form Score
                  </Typography>
                  <Chip
                    label={`${formCheckResults?.score}%`}
                    color={
                      formCheckResults?.score >= 80 ? 'success' :
                      formCheckResults?.score >= 60 ? 'warning' : 'error'
                    }
                  />
                </Box>
              </Grid>

              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Analysis
                </Typography>
                {formCheckResults?.analysis && (
                  <FormAnalysis analysis={formCheckResults.analysis} />
                )}
              </Grid>

              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Feedback
                </Typography>
                {formCheckResults?.feedback && (
                  <FormFeedback feedback={formCheckResults.feedback} />
                )}
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setViewResults(false)}>Close</Button>
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={() => {
                saveFormCheckFeedback(currentCheck, formCheckResults);
                setViewResults(false);
              }}
            >
              Save Results
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default FormChecking;
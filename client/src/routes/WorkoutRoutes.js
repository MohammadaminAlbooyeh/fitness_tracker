import React from 'react';
import { Routes, Route } from 'react-router-dom';
import WorkoutTemplateList from '../components/workout/WorkoutTemplateList';
import ScheduledWorkoutList from '../components/workout/ScheduledWorkoutList';
import PrivateRoute from './PrivateRoute';

const WorkoutRoutes = () => {
  return (
    <Routes>
      <Route 
        path="templates" 
        element={
          <PrivateRoute>
            <WorkoutTemplateList />
          </PrivateRoute>
        } 
      />
      <Route 
        path="scheduled" 
        element={
          <PrivateRoute>
            <ScheduledWorkoutList />
          </PrivateRoute>
        } 
      />
    </Routes>
  );
};

export default WorkoutRoutes;
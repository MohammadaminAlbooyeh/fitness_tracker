import React from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  LinearProgress
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { useQuery } from 'react-query';
import { getEquipmentStats } from '../../api/equipment';

const COLORS = ['#4caf50', '#2196f3', '#ff9800', '#f44336'];

const StatCard = ({ title, value, total, color }) => (
  <Paper sx={{ p: 2, height: '100%' }}>
    <Typography variant="h6" gutterBottom>
      {title}
    </Typography>
    <Typography variant="h4" color={color}>
      {value}
    </Typography>
    {total && (
      <Box sx={{ mt: 1 }}>
        <LinearProgress
          variant="determinate"
          value={(value / total) * 100}
          sx={{
            height: 8,
            borderRadius: 4,
            backgroundColor: '#e0e0e0',
            '& .MuiLinearProgress-bar': {
              backgroundColor: color
            }
          }}
        />
        <Typography variant="body2" color="textSecondary" sx={{ mt: 0.5 }}>
          {Math.round((value / total) * 100)}% of total
        </Typography>
      </Box>
    )}
  </Paper>
);

const EquipmentStats = () => {
  const { data: stats, isLoading } = useQuery('equipmentStats', getEquipmentStats);

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  const statusData = [
    { name: 'Available', value: stats.available_count },
    { name: 'In Use', value: stats.in_use_count },
    { name: 'Maintenance', value: stats.maintenance_count },
    { name: 'Out of Order', value: stats.out_of_order_count }
  ];

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Summary Stats */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Equipment"
            value={stats.total_equipment}
            color="primary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Available"
            value={stats.available_count}
            total={stats.total_equipment}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="In Use"
            value={stats.in_use_count}
            total={stats.total_equipment}
            color="#2196f3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Maintenance Due"
            value={stats.maintenance_due_count}
            total={stats.total_equipment}
            color="#f44336"
          />
        </Grid>

        {/* Usage Stats */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              Equipment Status Distribution
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  outerRadius={120}
                  label={({
                    cx,
                    cy,
                    midAngle,
                    innerRadius,
                    outerRadius,
                    value,
                    index
                  }) => {
                    const RADIAN = Math.PI / 180;
                    const radius = 25 + innerRadius + (outerRadius - innerRadius);
                    const x = cx + radius * Math.cos(-midAngle * RADIAN);
                    const y = cy + radius * Math.sin(-midAngle * RADIAN);

                    return (
                      <text
                        x={x}
                        y={y}
                        fill="#666"
                        textAnchor={x > cx ? 'start' : 'end'}
                        dominantBaseline="central"
                      >
                        {`${statusData[index].name} (${value})`}
                      </text>
                    );
                  }}
                  dataKey="value"
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Usage Hours */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '400px' }}>
            <Typography variant="h6" gutterBottom>
              Equipment Usage Overview
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body1">
                Total Usage Hours: {stats.total_usage_hours.toFixed(1)}
              </Typography>
              <Typography variant="body1">
                Average Usage per Equipment: {
                  (stats.total_usage_hours / stats.total_equipment).toFixed(1)
                } hours
              </Typography>
              <Typography variant="body1">
                Equipment Requiring Maintenance: {stats.maintenance_due_count}
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default EquipmentStats;
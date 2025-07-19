import React, { useEffect, useState } from "react";
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  Paper,
  List,
  ListItem,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  MenuItem,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Alert,
  IconButton,
  Tooltip,
  Divider,
  LinearProgress
} from "@mui/material";
import {
  Flight as FlightIcon,
  Warning as WarningIcon,
  Refresh as RefreshIcon,
  Add as AddIcon,
  Timeline as TimelineIcon,
  Speed as SpeedIcon,
  Height as HeightIcon,
  Schedule as ScheduleIcon
} from "@mui/icons-material";
import { getAirspace, getFlights, addFlight, getConflicts, suggestPath, getStats } from "./api";

interface Waypoint {
  name: string;
  latitude: number;
  longitude: number;
  type: string;
}
interface Route {
  from: string;
  to: string;
  distance: number;
  airway: string;
  direction: string;
}
interface Flight {
  callsign: string;
  route: string[];
  speed: number;
  flight_level: number;
  entry_time: string;
  timeline: Record<string, string>;
}
interface Conflict {
  type: string;
  flight1: string;
  flight2: string;
  [key: string]: any;
}
interface Stats {
  waypoints_count: number;
  flights_count: number;
  conflicts_count: number;
  conflict_types: Record<string, number>;
  routes_count: number;
}

const FLIGHT_LEVELS = Array.from({length: 13}, (_,i) => 290 + i*10);

function App() {
  const [waypoints, setWaypoints] = useState<Waypoint[]>([]);
  const [routes, setRoutes] = useState<Route[]>([]);
  const [flights, setFlights] = useState<Flight[]>([]);
  const [conflicts, setConflicts] = useState<Conflict[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    callsign: "",
    route: "A,B",
    speed: 450,
    flight_level: 330,
    entry_time: "2023-01-01T08:00:00"
  });
  const [suggestDialog, setSuggestDialog] = useState<{
    open: boolean, 
    callsign: string, 
    start: string, 
    goal: string, 
    result?: {
      new_path: string[],
      total_distance_nm: number,
      waypoints_count: number,
      original_start: string,
      original_goal: string
    }
  }>({open: false, callsign: "", start: "", goal: ""});

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [airspaceRes, flightsRes, conflictsRes, statsRes] = await Promise.all([
        getAirspace(),
        getFlights(),
        getConflicts(),
        getStats()
      ]);
      setWaypoints(airspaceRes.data.waypoints);
      setRoutes(airspaceRes.data.routes);
      setFlights(flightsRes.data);
      setConflicts(conflictsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddFlight = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await addFlight({
        ...form,
        route: form.route.split(",").map(s => s.trim()),
      });
      setForm({ ...form, callsign: "" });
      loadData();
    } catch (error) {
      console.error('Error adding flight:', error);
    }
  };

  const handleLoadTestData = async () => {
    try {
      setLoading(true);
      // Call the test data endpoint
      await fetch('http://localhost:8000/load_test_data', { method: 'POST' });
      loadData();
    } catch (error) {
      console.error('Error loading test data:', error);
    }
  };

  const handleSuggest = async (callsign: string, start: string, goal: string) => {
    setSuggestDialog({open: true, callsign, start, goal});
    try {
      const res = await suggestPath({callsign, start, goal});
      setSuggestDialog(d => ({...d, result: res.data}));
    } catch (error) {
      console.error('Error suggesting path:', error);
      setSuggestDialog(d => ({...d, result: undefined}));
    }
  };

  const getConflictColor = (type: string) => {
    switch (type) {
      case 'crossing': return 'error';
      case 'head-on': return 'error';
      case 'overtake': return 'warning';
      case 'lateral': return 'info';
      default: return 'default';
    }
  };

  const getConflictIcon = (type: string) => {
    switch (type) {
      case 'crossing': return '⚠️';
      case 'head-on': return '🚨';
      case 'overtake': return '⚡';
      case 'lateral': return '📏';
      default: return '❓';
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{mt: 4, mb: 4}}>
        <LinearProgress />
        <Typography variant="h6" sx={{mt: 2}}>Loading Air Traffic Control System...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{mt: 4, mb: 4}}>
      {/* Header */}
      <Box sx={{mb: 4, textAlign: 'center'}}>
        <Typography variant="h3" gutterBottom sx={{fontWeight: 'bold', color: 'primary.main'}}>
          🛩️ Air Traffic Control System
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Real-time Conflict Detection & Resolution
        </Typography>
      </Box>

      {/* Stats Dashboard */}
      {stats && (
        <Grid container spacing={2} sx={{mb: 4}}>
          <Grid item xs={12} md={3}>
            <Card sx={{bgcolor: 'primary.light', color: 'white'}}>
              <CardContent>
                <Typography variant="h4">{stats.waypoints_count}</Typography>
                <Typography variant="body2">Waypoints</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card sx={{bgcolor: 'success.light', color: 'white'}}>
              <CardContent>
                <Typography variant="h4">{stats.flights_count}</Typography>
                <Typography variant="body2">Active Flights</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card sx={{bgcolor: conflicts.length > 0 ? 'error.light' : 'success.light', color: 'white'}}>
              <CardContent>
                <Typography variant="h4">{stats.conflicts_count}</Typography>
                <Typography variant="body2">Conflicts Detected</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card sx={{bgcolor: 'info.light', color: 'white'}}>
              <CardContent>
                <Typography variant="h4">{stats.routes_count}</Typography>
                <Typography variant="body2">Routes</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Action Buttons */}
      <Box sx={{mb: 3, display: 'flex', gap: 2, justifyContent: 'center'}}>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={loadData}
        >
          Refresh Data
        </Button>
        <Button
          variant="outlined"
          color="secondary"
          onClick={handleLoadTestData}
        >
          Load Test Data
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Waypoints & Routes */}
        <Grid item xs={12} md={4}>
          <Paper sx={{p: 3, height: 'fit-content'}} elevation={3}>
            <Typography variant="h6" gutterBottom sx={{display: 'flex', alignItems: 'center', gap: 1}}>
              📍 Waypoints ({waypoints.length})
            </Typography>
            <List dense sx={{maxHeight: 300, overflow: 'auto'}}>
              {waypoints.map(wp => (
                <ListItem key={wp.name} sx={{border: '1px solid #e0e0e0', borderRadius: 1, mb: 1}}>
                  <ListItemText
                    primary={<strong>{wp.name}</strong>}
                    secondary={`${wp.latitude.toFixed(4)}, ${wp.longitude.toFixed(4)}`}
                  />
                  <Chip label={wp.type} size="small" color="primary" />
                </ListItem>
              ))}
            </List>

            <Divider sx={{my: 2}} />

            <Typography variant="h6" gutterBottom>
              🛣️ Routes ({routes.length})
            </Typography>
            <List dense sx={{maxHeight: 200, overflow: 'auto'}}>
              {routes.slice(0, 10).map((r,i) => (
                <ListItem key={i} sx={{border: '1px solid #e0e0e0', borderRadius: 1, mb: 1}}>
                  <ListItemText
                    primary={`${r.from} → ${r.to}`}
                    secondary={`${r.distance}NM • ${r.airway}`}
                  />
                </ListItem>
              ))}
              {routes.length > 10 && (
                <ListItem>
                  <ListItemText primary={`... and ${routes.length - 10} more routes`} />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>

        {/* Flights & Add Flight */}
        <Grid item xs={12} md={4}>
          <Paper sx={{p: 3, height: 'fit-content'}} elevation={3}>
            <Typography variant="h6" gutterBottom sx={{display: 'flex', alignItems: 'center', gap: 1}}>
              ✈️ Flights ({flights.length})
            </Typography>
            <List dense sx={{maxHeight: 400, overflow: 'auto'}}>
              {flights.map(f => (
                <ListItem key={f.callsign} sx={{border: '1px solid #e0e0e0', borderRadius: 1, mb: 1}}>
                  <ListItemText
                    primary={
                      <Box sx={{display: 'flex', alignItems: 'center', gap: 1}}>
                        <FlightIcon color="primary" />
                        <strong>{f.callsign}</strong>
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2">Route: {f.route.join(" → ")}</Typography>
                        <Box sx={{display: 'flex', gap: 1, mt: 1}}>
                          <Chip icon={<HeightIcon />} label={`FL${f.flight_level}`} size="small" />
                          <Chip icon={<SpeedIcon />} label={`${f.speed} KTS`} size="small" />
                        </Box>
                        <Typography variant="caption" display="block" sx={{mt: 1}}>
                          Entry: {new Date(f.entry_time).toLocaleTimeString()}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
              ))}
            </List>

            <Divider sx={{my: 2}} />

            <Typography variant="h6" gutterBottom sx={{display: 'flex', alignItems: 'center', gap: 1}}>
              <AddIcon /> Add Flight
            </Typography>
            <Box component="form" onSubmit={handleAddFlight}>
              <TextField
                label="Callsign"
                value={form.callsign}
                onChange={e=>setForm(f=>({...f, callsign: e.target.value}))}
                fullWidth
                margin="dense"
                required
                size="small"
              />
              <TextField
                label="Route (A,B,C)"
                value={form.route}
                onChange={e=>setForm(f=>({...f, route: e.target.value}))}
                fullWidth
                margin="dense"
                required
                size="small"
              />
              <TextField
                label="Speed (KTS)"
                type="number"
                value={form.speed}
                onChange={e=>setForm(f=>({...f, speed: +e.target.value}))}
                fullWidth
                margin="dense"
                required
                size="small"
              />
              <TextField
                label="Flight Level"
                select
                value={form.flight_level}
                onChange={e=>setForm(f=>({...f, flight_level: +e.target.value}))}
                fullWidth
                margin="dense"
                required
                size="small"
              >
                {FLIGHT_LEVELS.map(fl => <MenuItem key={fl} value={fl}>FL{fl}</MenuItem>)}
              </TextField>
              <TextField
                label="Entry Time"
                type="datetime-local"
                value={form.entry_time.slice(0,16)}
                onChange={e=>setForm(f=>({...f, entry_time: e.target.value}))}
                fullWidth
                margin="dense"
                required
                size="small"
              />
              <Button type="submit" variant="contained" sx={{mt: 2, width: '100%'}}>
                Add Flight
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Conflicts */}
        <Grid item xs={12} md={4}>
          <Paper sx={{p: 3, height: 'fit-content'}} elevation={3}>
            <Typography variant="h6" gutterBottom sx={{display: 'flex', alignItems: 'center', gap: 1}}>
              <WarningIcon color="error" />
              Conflicts ({conflicts.length})
            </Typography>

            {conflicts.length === 0 ? (
              <Alert severity="success" sx={{mb: 2}}>
                No conflicts detected! Airspace is safe.
              </Alert>
            ) : (
              <Alert severity="warning" sx={{mb: 2}}>
                {conflicts.length} conflicts detected. Review and resolve.
              </Alert>
            )}

            <List dense sx={{maxHeight: 500, overflow: 'auto'}}>
              {conflicts.map((c,i) => (
                <ListItem key={i} sx={{border: '1px solid #e0e0e0', borderRadius: 1, mb: 1}}>
                  <ListItemText
                    primary={
                      <Box sx={{display: 'flex', alignItems: 'center', gap: 1}}>
                        <span>{getConflictIcon(c.type)}</span>
                        <Chip
                          label={c.type.toUpperCase()}
                          color={getConflictColor(c.type) as any}
                          size="small"
                        />
                      </Box>
                    }
                    secondary={
                      <Box sx={{mt: 1}}>
                        <Typography variant="body2">
                          <strong>{c.flight1}</strong> & <strong>{c.flight2}</strong>
                        </Typography>
                        <Typography variant="caption" display="block">
                          FL{c.flight_level1} & FL{c.flight_level2}
                        </Typography>

                        {c.type === 'crossing' && (
                          <Typography variant="caption" display="block">
                            Waypoint: {c.waypoint}
                          </Typography>
                        )}
                        {c.type === 'head-on' && (
                          <Typography variant="caption" display="block">
                            Segment: {c.segment.join(' → ')}
                          </Typography>
                        )}
                        {c.type === 'overtake' && (
                          <Typography variant="caption" display="block">
                            Segment: {c.segment.join(' → ')}
                          </Typography>
                        )}
                        {c.type === 'lateral' && (
                          <Typography variant="caption" display="block">
                            At: {c.wp1} & {c.wp2}
                          </Typography>
                        )}

                        <Button
                          size="small"
                          variant="outlined"
                          sx={{mt: 1}}
                          onClick={()=>handleSuggest(c.flight1, flights.find(f=>f.callsign===c.flight1)?.route[0]||"", flights.find(f=>f.callsign===c.flight1)?.route.slice(-1)[0]||"")}
                        >
                          Suggest Path
                        </Button>
                      </Box>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Suggest Path Dialog */}
      <Dialog open={suggestDialog.open} onClose={()=>setSuggestDialog(d=>({...d, open:false, result:undefined}))} maxWidth="sm" fullWidth>
        <DialogTitle>Suggested Path for {suggestDialog.callsign}</DialogTitle>
        <DialogContent>
          {suggestDialog.result ? (
            <Alert severity="success">
              <Typography variant="h6">New Path Found!</Typography>
              <Typography>Route: {suggestDialog.result.new_path.join(" → ")}</Typography>
              <Typography>Total Distance: {suggestDialog.result.total_distance_nm.toFixed(2)} NM</Typography>
              <Typography>Waypoints: {suggestDialog.result.waypoints_count}</Typography>
              <Typography>Original Start: {suggestDialog.result.original_start}</Typography>
              <Typography>Original Goal: {suggestDialog.result.original_goal}</Typography>
            </Alert>
          ) : (
            <Box sx={{display: 'flex', alignItems: 'center', gap: 2}}>
              <LinearProgress />
              <Typography>Finding alternative path...</Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={()=>setSuggestDialog(d=>({...d, open:false, result:undefined}))}>Close</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default App;

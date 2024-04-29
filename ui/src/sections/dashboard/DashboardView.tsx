import { Button, Grid, Stack } from "@mui/material";
import Paper from "@mui/material/Paper";
import { styled } from "@mui/material/styles";
import "./styles/DashboardView.css";

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));

export default function DashboardView() {
  return (
    <Grid
      container
      spacing={2}
      direction="column"
      justifyContent="center"
      alignItems="center"
      style={{ minHeight: "100vh" }} // This makes the Grid container take up the full height of the viewport
    >
      <Grid item xs={8}>
        <Stack direction="column" spacing={2}>
          <Button variant="contained">Pay</Button>
        </Stack>
      </Grid>
      <Grid item xs={4}>
        <Stack direction="column" spacing={2}>
          <Button variant="contained">Sui Version</Button>
        </Stack>
      </Grid>
      <Grid item xs={4}>
        <Stack direction="column" spacing={2}>
          <Button variant="contained">adress</Button>
        </Stack>
      </Grid>
      <Grid item xs={8}>
        <Stack direction="column" spacing={2}>
          <Button variant="contained">envs</Button>
        </Stack>
      </Grid>
    </Grid>
  );
}

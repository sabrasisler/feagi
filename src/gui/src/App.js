import React, { useState, useEffect } from "react";
import { Route, Routes, Navigate, useNavigate } from "react-router-dom";
import AccessAlarmIcon from "@mui/icons-material/AccessAlarm";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import CameraAltIcon from "@mui/icons-material/CameraAlt";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import MenuIcon from "@mui/icons-material/Menu";
import ReplayIcon from "@mui/icons-material/Replay";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Environment from "./routes/Environment";
import GenomeAssembler from "./routes/GenomeAssembler";
import GenomeMode from "./routes/GenomeMode";
import CorticalAreaEditor from "./routes/CorticalAreaEditor";
import Mapping from "./routes/Mapping";
import Sensorimotor from "./routes/Sensorimotor";
import MonitoringDashboard from "./routes/MonitoringDashboard";
import PhysicalRobots from "./routes/PhysicalRobots";
import DefaultGenomes from "./routes/DefaultGenomes";
// import ProgressStepper from "./components/ProgressStepper";
import FeagiAPI from "./services/FeagiAPI";

function App() {
  const [definedMotor, setDefinedMotor] = useState([]);
  const [selectedMotor, setSelectedMotor] = useState([]);
  const [definedSensory, setDefinedSensory] = useState([]);
  const [selectedSensory, setSelectedSensory] = useState([]);
  const [definedMappings, setDefinedMappings] = useState([]);
  const [customAreas, setCustomAreas] = useState([]);
  const [definedAreas, setDefinedAreas] = useState([]);
  const [defaultMorphologyScalarX, setDefaultMorphologyScalarX] =
    useState(null);
  const [defaultMorphologyScalarY, setDefaultMorphologyScalarY] =
    useState(null);
  const [defaultMorphologyScalarZ, setDefaultMorphologyScalarZ] =
    useState(null);
  const [defaultPscMultiplier, setDefaultPscMultiplier] = useState(null);
  const [defaultPlasticityFlag, setDefaultPlasticityFlag] = useState(null);
  const [defaultSynapseRules, setDefaultSynapseRules] = useState(null);
  const [defaultCorticalGenes, setDefaultCorticalGenes] = useState({});
  const [defaultGenomeData, setDefaultGenomeData] = useState({});
  const [drawerOpen, setDrawerOpen] = useState(false);
  let navigate = useNavigate();

  const currentDomain = window.location.href;
  if (currentDomain.includes("127.0.0.1:3000")) {
    const redirectDomain = currentDomain.replace(
      "127.0.0.1:3000",
      "localhost:3000"
    );
    window.location.replace(redirectDomain);
  }

  useEffect(() => {
    FeagiAPI.getBaselineCorticalGenes().then((items) =>
      setDefaultCorticalGenes(items)
    );

    FeagiAPI.getBaselineMorphology().then((rules) =>
      setDefaultSynapseRules(rules)
    );

    let defaultMorphologySetterArray = [
      setDefaultMorphologyScalarX,
      setDefaultMorphologyScalarY,
      setDefaultMorphologyScalarZ,
    ];
    FeagiAPI.getBaselineMorphologyScalar().then((items) =>
      items.forEach((item, index) => defaultMorphologySetterArray[index](item))
    );

    FeagiAPI.getBaselinePscMultiplier().then((multiplier) =>
      setDefaultPscMultiplier(multiplier)
    );

    FeagiAPI.getBaselinePlasticityFlag().then((flag) =>
      setDefaultPlasticityFlag(flag)
    );

    FeagiAPI.getDefaultGenomes().then((response) => {
      setDefaultGenomeData(response["genomes"]);
    });
  }, []);

  const appTheme = createTheme({
    palette: {
      background: {
        default: "#ebe8e8",
      },
    },
  });

  const handleMenuClick = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleGenomeReload = () => {
    navigate("/genome/mode");
  };

  const handleContributeClick = () => {};

  const handleApiDocsClick = () => {
    window.open("http://localhost:8000/docs", "_blank", "noopener,noreferrer");
  };

  const handleHelpClick = () => {
    window.open(
      "https://github.com/feagi/feagi#readme",
      "_blank",
      "noopener,noreferrer"
    );
  };

  const drawerList = () => (
    <Box
      sx={{ width: "400px" }}
      role="presentation"
      onClick={() => setDrawerOpen(false)}
      onKeyDown={() => setDrawerOpen(false)}
    >
      <List>
        {/* <ListItem button>
          <ListItemIcon>
            <AccessAlarmIcon />
          </ListItemIcon>
          <ListItemText primary="Change Burst Frequency" />
        </ListItem>
        <Divider />
        <ListItem button>
          <ListItemIcon>
            <CameraAltIcon />
          </ListItemIcon>
          <ListItemText primary="Take Connectome Snapshot" />
        </ListItem>
        <Divider /> */}
        <ListItem button onClick={handleGenomeReload}>
          <ListItemIcon>
            <ReplayIcon />
          </ListItemIcon>
          <ListItemText primary="Reload Genome" />
        </ListItem>
        <Divider />
      </List>
    </Box>
  );

  return (
    <>
      <ThemeProvider theme={appTheme}>
        <CssBaseline />
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <IconButton
                color="inherit"
                onClick={handleMenuClick}
                edge="start"
              >
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" sx={{ ml: 4, flexGrow: 1 }}>
                Framework for Evolutionary Artificial General Intelligence
                (FEAGI)
              </Typography>
              <div
                style={{
                  display: "flex",
                  justifyContent: "right",
                  alignItems: "right",
                }}
              >
                {/* <Button
                  variant="text"
                  color="inherit"
                  onClick={handleContributeClick}
                >
                  Contribute
                </Button> */}
                <Button
                  variant="text"
                  color="inherit"
                  onClick={handleApiDocsClick}
                >
                  API Docs
                </Button>
                <Button
                  variant="text"
                  color="inherit"
                  onClick={handleHelpClick}
                >
                  Help
                </Button>
              </div>
            </Toolbar>
          </AppBar>
        </Box>
        <Drawer
          anchor="left"
          variant="temporary"
          elevation={3}
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
        >
          <Box textAlign="center" role="presentation">
            <Typography variant="h5" component="div" sx={{ m: 2 }}>
              Configuration
            </Typography>
            <Divider />
          </Box>
          {drawerList()}
        </Drawer>
        <Routes>
          <Route path="/" element={<Navigate replace to="/environment" />} />
          <Route path="/environment" element={<Environment />} />
          <Route path="/robot/physical" element={<PhysicalRobots />} />
          <Route path="/genome/mode" element={<GenomeMode />} />
          <Route
            path="/genome/defaults"
            element={<DefaultGenomes defaultGenomeData={defaultGenomeData} />}
          />
          <Route
            path="/genome/assemble"
            element={
              <GenomeAssembler
                definedMotor={definedMotor}
                definedSensory={definedSensory}
                definedMappings={definedMappings}
                definedAreas={definedAreas}
              />
            }
          />
          <Route
            path="/brain/mapping"
            element={
              <Mapping
                definedMappings={definedMappings}
                setDefinedMappings={setDefinedMappings}
                definedSensory={definedSensory}
                definedMotor={definedMotor}
                definedAreas={definedAreas}
                setDefinedAreas={setDefinedAreas}
                defaultMorphologyScalarX={defaultMorphologyScalarX}
                defaultMorphologyScalarY={defaultMorphologyScalarY}
                defaultMorphologyScalarZ={defaultMorphologyScalarZ}
                defaultPscMultiplier={defaultPscMultiplier}
                defaultPlasticityFlag={defaultPlasticityFlag}
                defaultSynapseRules={defaultSynapseRules}
              />
            }
          />
          <Route
            path="/brain/editor"
            element={
              <CorticalAreaEditor
                selectedSensory={selectedSensory}
                setSelectedSensory={setSelectedSensory}
                definedSensory={definedSensory}
                setDefinedSensory={setDefinedSensory}
                selectedMotor={selectedMotor}
                definedMotor={definedMotor}
                setDefinedMotor={setDefinedMotor}
                customAreas={customAreas}
                setCustomAreas={setCustomAreas}
                definedAreas={definedAreas}
                setDefinedAreas={setDefinedAreas}
                defaultCorticalGenes={defaultCorticalGenes}
              />
            }
          />
          <Route
            path="/brain/sensorimotor"
            element={
              <Sensorimotor
                selectedSensory={selectedSensory}
                setSelectedSensory={setSelectedSensory}
                definedSensory={definedSensory}
                setDefinedSensory={setDefinedSensory}
                selectedMotor={selectedMotor}
                setSelectedMotor={setSelectedMotor}
                definedMotor={definedMotor}
                setDefinedMotor={setDefinedMotor}
                definedAreas={definedAreas}
                setDefinedAreas={setDefinedAreas}
                defaultCorticalGenes={defaultCorticalGenes}
              />
            }
          />
          <Route path="/monitoring" element={<MonitoringDashboard />} />
        </Routes>
        {/* <div
          style={{
            position: "absolute",
            left: "50px",
            bottom: "50px",
            right: "50px",
          }}
        >
          <ProgressStepper />
        </div> */}
      </ThemeProvider>
    </>
  );
}

export default App;

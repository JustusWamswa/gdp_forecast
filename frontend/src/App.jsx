import React, { useEffect, useState } from 'react'
import { Box, Button, createTheme, Stack, ThemeProvider, Typography, useMediaQuery } from '@mui/material'
import Feature from '../components/Feature'
import { green, purple } from '@mui/material/colors';
import './App.css'
import GDPChart from '../components/GDPChart';
import { textfields } from '../cache/cache';

function App() {

  const theme = createTheme({
    palette: {
      primary: {
        main: '#02B2AF',
      },
      secondary: {
        main: green[500],
      },
    },
  });

  const [features, setFeatures] = useState(textfields)
  const [interpolationYear, setInterpolationYear] = useState(0)
  const [predictedGDP, setPredictedGDP] = useState(0)
  const [debouncedQuery, setDebouncedQuery] = useState(features)
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const api = import.meta.env.VITE_API

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(features);
    }, 500);

    return () => clearTimeout(handler);
  }, [features]);

  useEffect(() => {
    if (debouncedQuery) {
      // Make API request
      handlePredict()
      // console.log('API Request:', debouncedQuery);
    }
  }, [debouncedQuery]);

  // console.log("Prediction: ", predictedGDP)

  const handlePredict = async () => {
    const featureValues = features.map((feature) => {
      return feature.value
    })
    const payload = { "inputs": featureValues }
    console.log(payload)
    try {
      const res = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      setPredictedGDP(data?.prediction)
      features.forEach(feature => {
        if(feature?.name.toLowerCase() === 'year') {
          setInterpolationYear(feature.value)
        }
      })
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <ThemeProvider theme={theme}>
      <Box maxWidth={'90%'} mx={'auto'}>
        <Typography color='primary.dark' fontWeight={'bold'} variant='h5' py={2}>GDP Forecasting Tool</Typography>
        <Stack direction={isMobile ? 'column' : 'row'} justifyContent={'space-evenly'}>
          <Box width={isMobile ? '100%' : '50%'}>
            <Box bgcolor={'rgba(2,178,175,0.08)'} minHeight={'60vh'} px={isMobile ? 1 : 5} py={2} borderRadius={5} mb={1}>
              <Typography variant='subtitle2'>Forecasted GDP</Typography>
              <Typography variant='h4' >{(predictedGDP / 1e+9).toFixed(2)} B</Typography>
              <GDPChart prediction={predictedGDP} predictionYear={interpolationYear} />
            </Box>
            <Typography fontStyle={'italic'} variant='caption' >
              The primary sector comprises "Agriculture, forestry and fishing" and "Mining and quarrying" <br />
              The secondary sector includes "Manufacturing", "Electricity, gas, steam and air conditioning supply", "Water supply; sewerage, waste management and remediation activities" 
              and "Construction" <br />
              The tertiary sector includes "Wholesale and retail trade; repair of motor vehicles and motorcycles", "Transportation and storage", "Accomodation and food service activities", 
              "Information and communication", "Financial and insurance activities", "Real estate activities", "Professional, scientific and technical activities", "Administrative and support service activities", 
              "Public administration and defence; compulsory social security", "Education", "Human health and social work", "Arts, entertainment, recreation", and "Other services activities" <br />
              * All currencies are in Mauritian Rupees (Rs)
            </Typography>
          </Box>
          <Box width={isMobile ? '100%' : '30%'} marginTop={isMobile && 5}>
            <Typography variant='subtitle2' gutterBottom pb={2}>
              Adjust parameters using the text boxes or sliders below:
            </Typography>
            <Box mb={3} maxHeight={'75vh'} px={3} sx={{ overflowY: 'scroll' }} >
              {features.map((feature) => (
                <Feature key={feature.name} name={feature.name} value={feature.value} setFeatures={setFeatures} />
              ))}
            </Box>
          </Box>
        </Stack>
      </Box>
    </ThemeProvider>
  )
}

export default App

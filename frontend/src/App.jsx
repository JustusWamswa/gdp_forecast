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
    try {
      const res = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      setPredictedGDP(data?.prediction)
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <ThemeProvider theme={theme}>
      <Box maxWidth={'90%'} mx={'auto'}>
        <Typography color='primary.dark' fontWeight={'bold'} variant='h5' py={2}>GDP Forecasting Tool</Typography>
        <Stack direction={isMobile ? 'column' : 'row'} justifyContent={'space-evenly'}>
          <Box width={isMobile ? '100%' : '50%'} bgcolor={'rgba(2,178,175,0.08)'} px={isMobile ? 1 : 5} py={2} borderRadius={5}>
            <Typography variant='subtitle2'>Forecasted GDP</Typography>
            <Typography variant='h4' >{(predictedGDP/1e+9).toFixed(2)} B</Typography>
            <GDPChart prediction={predictedGDP} />
          </Box>
          <Box width={isMobile ? '100%' : '30%'} marginTop={isMobile && 5}>
            <Typography variant='subtitle2' gutterBottom pb={2}>
              Adjust parameters using the text boxes or sliders below:
            </Typography>
            <Box mb={3} maxHeight={'75vh'} px={3} sx={{ overflowY: 'scroll' }} >
              {features.map((feature) => (
                <Feature key={feature.name} name={feature.name} value={feature.value} setFeatures={setFeatures} />
              ))}
              {/* <Button
              variant='contained'
              fullWidth
              sx={{ color: 'white', textTransform: 'capitalize' }}
              onClick={handlePredict}
            >
              Predict GDP
            </Button> */}
            </Box>
          </Box>
        </Stack>
      </Box>
    </ThemeProvider>
  )
}

export default App

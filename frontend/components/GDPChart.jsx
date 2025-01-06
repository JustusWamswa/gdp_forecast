import React, { useEffect, useRef, useState } from 'react'
import { LineChart } from '@mui/x-charts/LineChart'
import { GDPHistoryData, GDPHistoryYears } from '../cache/cache'
import { useMediaQuery, useTheme } from '@mui/material'

function GDPChart(props) {
  const { prediction, predictionYear } = props
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const repeatedArray = Array(GDPHistoryData.length).fill(null)
  const predictionData = [...GDPHistoryData, prediction].map((data) => data == null ? null : (data / 1e+9).toFixed(2))

  const yearFormatter = (date) => date.getFullYear().toString()
  GDPHistoryYears[GDPHistoryYears.length - 1] = predictionYear
  const minYear = new Date(Math.min(...GDPHistoryYears), 0, 1)
  const maxYear = new Date(Math.max(...GDPHistoryYears) + 3, 0, 1)

  const chartContainerRef = useRef(null)
  const [chartSize, setChartSize] = useState({ width: 500, height: 400 })

  useEffect(() => {
    const updateChartSize = () => {
      if (chartContainerRef.current) {
        const containerWidth = chartContainerRef.current.offsetWidth;
        const containerHeight = chartContainerRef.current.offsetHeight;
        setChartSize({
          width: containerWidth * 0.9, // Adjust the width dynamically (90% of container)
          height: isMobile ? 300 : containerHeight * 0.8, // Dynamic height, reduced for mobile
        });
      }
    };

    // Update chart size on mount and on window resize
    updateChartSize();
    window.addEventListener('resize', updateChartSize);

    return () => {
      window.removeEventListener('resize', updateChartSize);
    };
  }, [isMobile, chartContainerRef]);

  return (
    <div ref={chartContainerRef} style={{ width: '100%', height: '100%' }}>
      <LineChart
        sx={{
          '& .MuiMarkElement-series-Forecast': {
            fill: '#fff',
            stroke: '#02B2AF',
            strokeWidth: 2,
          },
          '& .MuiLineElement-series-Forecast': {
            strokeDasharray: '10 5',
          },
          '& .MuiChartsAxis-label': {
            transform: 'translateX(-10px)',
          }
        }}
        xAxis={
          [
            {
              data: GDPHistoryYears.map(year => new Date(year, 0, 1)),
              label: 'Year',
              scaleType: 'time',
              valueFormatter: yearFormatter,
              min: minYear,
              max: maxYear,
            },
          ]}
        yAxis={
          [{
            label: 'GDP (Billions)',
          }]}
        series={
          [
            {
              data: predictionData,
              showMark: ({ index }) => index === predictionData.length - 1,
              label: 'Forecast',
              id: 'Forecast',
            },
            {
              data: GDPHistoryData.map((data) => (data / 1e+9).toFixed(2)),
              showMark: ({ index }) => index % 2 === 0,
              label: 'Historical',
            }
          ]}
        width={chartSize.width}
        height={chartSize.height}
      />
    </div>
  )
}

export default GDPChart
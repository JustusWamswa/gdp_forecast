import React from 'react'
import { LineChart } from '@mui/x-charts/LineChart'
import { GDPHistoryData, GDPHistoryYears } from '../cache/cache'
import { useMediaQuery, useTheme } from '@mui/material'

function GDPChart(props) {
  const { prediction } = props
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const repeatedArray = Array(GDPHistoryData.length).fill(null)
  const predictionData = [...GDPHistoryData, prediction].map((data) => data == null ? null : (data / 1e+9).toFixed(2))

  const yearFormatter = (date) => date.getFullYear().toString()

  return (
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
      xAxis = {
        [
        {
          data: GDPHistoryYears.map(year => new Date(year, 0, 1)),
          label: 'Year',
          scaleType: 'time',
          valueFormatter: yearFormatter
        },
            ]}
      yAxis = {
        [{
          label: 'GDP (Billions)',
        }]}
      series = {
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
      width = {isMobile ? 350 : 500}
      height = {isMobile ? 300 : 400}
    />
  )
}

export default GDPChart
import { Box, Input, Slider, Table, TableCell, TableRow, TextField, Typography } from '@mui/material'
import React, { useState } from 'react'

function Feature(props) {

    const {name, value, setFeatures} = props
    const [inputValue, setInputValue] = useState(value)

    const handleSliderChange = (event, newValue) => {
        setInputValue(newValue);
    }

    const handleInputChange = (event) => {
        setInputValue(event.target.value === '' ? 0 : Number(event.target.value))
        setFeatures((prevFeatures) =>
            prevFeatures.map((feature) =>
              feature.name === event.target.name ? { ...feature, value: Number(event.target.value) } : feature
            )
          );

    }

    const handleBlur = () => {
        if (inputValue < 0) {
            setInputValue(0);
        } else if (inputValue > 100) {
            setInputValue(100);
        }
    }

    return (
        <Box bgcolor={'#f1f1f1'} p={2} borderRadius={5} mb={2}>
            <Typography variant='caption' fontWeight={'bold'}>{name}</Typography>
            {/* <Table size='small' sx={{ marginY: 1 }}>
                <TableRow>
                    <TableCell sx={{ border: 0, p: 0 }}>Current Value:</TableCell>
                    <TableCell sx={{ border: 0, p: 0 }}>516.50 B</TableCell>
                </TableRow>
                <TableRow>
                    <TableCell sx={{ border: 0, p: 0 }}>Range:</TableCell>
                    <TableCell sx={{ border: 0, p: 0 }}>451 - 641 B</TableCell>
                </TableRow>
            </Table> */}

            <TextField
                value={inputValue}
                fullWidth
                
                // disableUnderline
                sx={{ mt: 1 }}
                size='small'
                onChange={handleInputChange}
                // onBlur={handleBlur}
                type='number'
                name={name}
                // inputProps={{
                //     step: 10,
                //     min: 0,
                //     max: 100,
                //     type: 'number',
                // }}
            />

            {/* <Slider
                size="small"
                valueLabelDisplay="auto"
                color="primary"
                value={typeof value === 'number' ? value : 0}
                onChange={handleSliderChange}
            /> */}
        </Box>
    )
}

export default Feature
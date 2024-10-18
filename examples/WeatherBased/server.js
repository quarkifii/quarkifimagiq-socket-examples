const express = require('express')
const path = require('path')
const axios = require('axios')
const crypto = require('crypto')

const app = express()
const PORT = process.env.PORT || 3000

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')))

// Middleware to parse JSON bodies
app.use(express.json())


const apiKey = '__COLLECT_API_KEY_FROM_MAGIQ_STORE__'
const secretKey = '__COLLECT_SECRET_KEY_FROM_MAGIQ_STORE__'


async function deviceOnOff(deviceId, operation) {
    console.log('deviceOnOff : ', deviceId, operation)
    try {
        const requestData = {
            deviceId: deviceId,
            action: 'SET',
            device: {
                deviceId: deviceId,
                deviceChangeCounter: 10,
                deviceState: {
                    "switch_1": operation ? '1' : '0'
                }
            },
        }

        const timestamp = new Date().toISOString()
        const content = apiKey + timestamp
        const signature = crypto.createHmac('sha256', secretKey).update(content).digest('hex')

        const serviceUrl = `https://api.magiqworks.com/api-ext-magiq/device`
        const headers = {
            'MQ-TIMESTAMP': timestamp,
            'MQ-API-KEY': apiKey,
            'MQ-SIGNATURE': signature,
            'Content-Type': 'application/json'
        }

        const postResponse = await axios.post(serviceUrl, requestData, { headers })
        return postResponse.data

    } catch(error) {
        console.error('Error in deviceOnOff:', error)
        throw error
    }
}

// Endpoint to fetch weather data
app.get('/api/weather/:lat/:lon', async (req, res) => {
    const { lat, lon } = req.params
    console.log('received lat and lon ', lat, lon)

    const options = {
        method: 'GET',
        url: `https://open-weather13.p.rapidapi.com/city/latlon/${lat}/${lon}`,
        headers: {
          'x-rapidapi-key': '__COLLECT_API_KEY_FROM_rapidapi__',
          'x-rapidapi-host': 'open-weather13.p.rapidapi.com'
        }
      };

    try {
        const response = await axios.request(options)
        res.json(response.data)
    } catch(error) {
        console.error(error)
        res.status(500).json({ error: 'An error occurred while fetching weather data.' })
    }
})

// Endpoint to handle device operations
app.post('/api/device', async (req, res) => {
    const { deviceId, operation } = req.body

    try {
        const response = await deviceOnOff(deviceId, operation)
        res.json(response)
    } catch(error) {
        res.status(500).json({ error: 'An error occurred while processing your request.' })
    }
})


// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'))
})

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`)
})

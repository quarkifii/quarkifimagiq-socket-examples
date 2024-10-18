const express = require('express')
const axios = require('axios')
const crypto = require('crypto')

const app = express()
const port = process.env.PORT || 3001

const apiKey = '__COLLECT_API_KEY_FROM_MAGIQ_STORE__'
const secretKey = '__COLLECT_SECRET_KEY_FROM_MAGIQ_STORE__'

// Middleware to parse JSON requests
app.use(express.json())

// Endpoint to turn the device on or off
app.post('/api/device-on-off', async (req, res) => {
  const { deviceId, operation } = req.body
  console.log('request body : : ', req.body)

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

    try {
      const postResponse = await axios.post(serviceUrl, requestData, { headers })
      return postResponse.data
    } catch(error) {
      console.error('Error in deviceOnOff:', error)
      throw error
    }

  } catch(parseError) {
    console.error('Error parsing device response:', parseError)
    throw parseError
  }
})

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`)
})

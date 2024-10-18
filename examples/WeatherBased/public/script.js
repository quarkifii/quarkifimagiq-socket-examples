let lat, lon, previousCircle
let hotTemp = 26
let lowHumidity = 25
let highHumidity = 80

const customizeTemperatures = dropdown => {
  hotTemp = parseInt(dropdown.value, 10)
}

const getLocation = () => 
  new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(resolve, reject)
    } else {
      reject(new Error('Geolocation is not supported by this browser.'))
    }
  })

const getWeather = async (lat, lon) => {
  try {
    const response = await axios.get(`/api/weather/${lat}/${lon}`)
    return response.data
  } catch (error) {
    console.error(error)
  }
}

const updateWeatherCircle = async (temp, humidity) => {
  temp = (temp - 273.15).toFixed(1)
  humidity = humidity.toFixed(1)
  const weatherCircle = document.getElementById('weatherCircle')
  const message = document.getElementById('message')
  message.style.display = 'block'
  let currentCircle

  if (temp < (hotTemp - 6)) {
    currentCircle = 'cold'
  } else if (temp > hotTemp) {
    currentCircle = 'hot'
  } else {
    currentCircle = 'good'
  }

  if (currentCircle !== previousCircle || (humidity < lowHumidity || humidity > highHumidity)) {
    weatherCircle.className = `circle ${currentCircle}`
    weatherCircle.textContent = `${currentCircle.charAt(0).toUpperCase() + currentCircle.slice(1)} ${temp}°C, ${humidity}%`

    if ((currentCircle === 'cold' && (humidity < lowHumidity || humidity > highHumidity)) ||
        (currentCircle === 'good' && (humidity < lowHumidity || humidity > highHumidity)) ||
        currentCircle === 'hot') {
      message.textContent = `Weather is ${currentCircle} with ${humidity}% humidity, so turn the AC On`
      await deviceOnOff('16612385', true)
    } else {
      message.textContent = `Weather is ${currentCircle} with ${humidity}% humidity, so turn the AC Off`
      await deviceOnOff('16612385', false)
    }
  }

  previousCircle = currentCircle
}

const deviceOnOff = async (deviceId, operation) => {
  try {
    const response = await axios.post('/api/device', { deviceId, operation })
    console.info('Device operation response:', response.data)
  } catch (error) {
    console.error('Error in deviceOnOff:', error)
  }
}

const init = async () => {
  try {
    const position = await getLocation()
    lat = position.coords.latitude
    lon = position.coords.longitude
    const weatherData = await getWeather(lat, lon)
    const temperature = weatherData?.main.temp 
    const humidity = weatherData?.main.humidity 
    await updateWeatherCircle(temperature, humidity)
  } catch (error) {
    console.error(error)
    document.getElementById('weatherCircle').textContent = '? 👇'
    document.getElementById('inputContainer').style.display = 'block'
  }
}

const getWeatherFromInput = async () => {
  lat = document.getElementById('latitude').value
  lon = document.getElementById('longitude').value
  if (lat && lon) {
    try {
      const weatherData = await getWeather(lat, lon)
      const temperature = weatherData?.main.temp 
      const humidity = weatherData?.main.humidity 
      await updateWeatherCircle(temperature, humidity)
    } catch (error) {
      console.error(error)
      document.getElementById('weatherCircle').textContent = '? 👇'
    }
  } else {
    alert('Please enter both latitude and longitude.')
  }
}

const generateTemperatureOptions = () => {
  const dropdown = document.getElementById('temperatureDropdown')
  for (let temp = 18; temp <= 50; temp++) {
    const option = document.createElement('option')
    option.value = temp
    option.textContent = `${temp}°C`
    dropdown.appendChild(option)
  }
  dropdown.value = 26
}

const generateHumidityOptions = () => {
  const lowHumidityDropdown = document.getElementById('lowHumidity')
  const highHumidityDropdown = document.getElementById('highHumidity')
  for (let humidity = 5; humidity <= 95; humidity += 5) {
    const option = document.createElement('option')
    option.value = humidity
    option.textContent = `${humidity}%`
    lowHumidityDropdown.appendChild(option.cloneNode(true))
    highHumidityDropdown.appendChild(option)
  }
  lowHumidityDropdown.value = 25
  highHumidityDropdown.value = 60
}

const customizeHumidityLimits = () => {
  lowHumidity = parseInt(document.getElementById('lowHumidity').value, 10)
  highHumidity = parseInt(document.getElementById('highHumidity').value, 10)
}

generateHumidityOptions()
generateTemperatureOptions()
init()

setInterval(async () => {
  if (lat && lon) {
    try {
      console.log('Low Humidity:', lowHumidity, 'High Humidity:', highHumidity, 'Hot Temp:', hotTemp)
      const weatherData = await getWeather(lat, lon)
      const temperature = weatherData?.main.temp 
      const humidity = weatherData?.main.humidity 
      await updateWeatherCircle(temperature, humidity)
    } catch (error) {
      console.error(error)
    }
  } else {
    init()
  }
}, 600000) // 10 minutes 

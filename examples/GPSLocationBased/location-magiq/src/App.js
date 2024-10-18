import React, { useState } from 'react'
import MapComponent from './MapComponent'

const App = () => {
  const [homeLocation, setHomeLocation] = useState(null)

  return (
    <div>
      <h1>Home Area Map</h1>
      <MapComponent homeLocation={ homeLocation } setHomeLocation={ setHomeLocation } />
    </div>
  )
}

export default App

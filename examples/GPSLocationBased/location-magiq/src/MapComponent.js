import React, { useState, useEffect } from "react"
import { Circle, MapContainer, TileLayer, useMap, useMapEvent } from "react-leaflet"
import CustomMarker from './customMarker'
import axios from 'axios'

export default function MapComponent() {
  const [currentLocation, setCurrentLocation] = useState(null)
  const [source, setSource] = useState(null)

  useEffect(() => {
    if(source && currentLocation) {
      console.log(source, currentLocation)
      const R = 6371e3 // metres
      const φ1 = currentLocation.lat * Math.PI / 180
      const φ2 = source.lat * Math.PI / 180
      const Δφ = (source.lat - currentLocation.lat) * Math.PI / 180
      const Δλ = (source.lng - currentLocation.lng) * Math.PI / 180

      const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
        Math.cos(φ1) * Math.cos(φ2) *
        Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

      const d = R * c
      console.log('->>>>>>',d)

      if(d <= 50) {
        axios.post('/api/device-on-off', {
          deviceId: 16612385,
          operation: true
        })
          .then(response => {
            console.log('Device turned on:', response.data)
          })
          .catch(error => {
            console.error('Error turning device on:', error)
          })
      } else {
        axios.post('/api/device-on-off', {
          deviceId: 16612385,
          operation: false
        })
          .then(response => {
            console.log('Device turned on:', response.data)
          })
          .catch(error => {
            console.error('Error turning device on:', error)
          })
      }
    }
  }, [source, currentLocation])

  const LocationMarker = () => {
    const map = useMap()

    useEffect(() => {
      map.locate({
        watch: true,
        setView: true,
        enableHighAccuracy: true
      }).on("locationfound", (e) => {
        setCurrentLocation(e.latlng)
      }).on("locationerror", (error) => {
        console.error("Error getting geolocation:", error)
      })
    }, [map])

    return currentLocation ? (
      <CustomMarker position={ currentLocation }>
        <p>You are here</p>
      </CustomMarker>
    ) : null
  }

  const SourceMarker = () => {
    const map = useMapEvent({
      click(e) {
        if(!source) {
          setSource(e.latlng)
        }
        map.flyTo(e.latlng, map.getZoom())
      }
    })

    return (
      source && <CustomMarker
        position={ source }
        onClick={ () => {
          setSource(null)
        } }>
        <Circle
          center={ source }
          pathOptions={ { fillColor: 'blue' } }
          radius={ 50 }
        />
        <Circle
          center={ source }
          pathOptions={ { fillColor: 'red' } }
          radius={ 40 }
          stroke={ false }
        />
      </CustomMarker>
    )
  }

  return (

    <MapContainer center={ null } zoom={ 17 }>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <LocationMarker />
      <SourceMarker />
    </MapContainer>
  )
}

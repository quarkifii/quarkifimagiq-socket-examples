import React from "react"
import { Marker } from "react-leaflet"
import L from "leaflet"
import "leaflet/dist/leaflet.css"
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

// Set default marker icon
const DefaultIcon = L.icon({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})

const CustomMarker = ({ position, onClick, children }) => {
  return (
    <Marker position={position} icon={DefaultIcon} eventHandlers={{ click: onClick }}>
      {children}
    </Marker>
  )
}

export default CustomMarker


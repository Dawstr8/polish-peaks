"use client";

import { useEffect, ReactNode } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import "leaflet/dist/leaflet.css";
import { initializeLeafletIcons, MAP_CONFIG } from "@/lib/leaflet";
import { cn } from "@/lib/utils";

interface LocationData {
  index: string | number;
  latitude: number;
  longitude: number;
  title: string;
  popupContent?: ReactNode;
  markerColor?: string;
}

interface LocationMapProps {
  locations: LocationData[];
  zoom?: number;
  height?: string;
  className?: string;
}

export function LocationMap({
  locations,
  zoom = MAP_CONFIG.DEFAULT_ZOOM,
  height = MAP_CONFIG.DEFAULT_HEIGHT,
  className = "",
}: LocationMapProps) {
  useEffect(() => {
    initializeLeafletIcons();
  }, []);

  const mapCenter: LatLngExpression = [
    locations[0].latitude,
    locations[0].longitude,
  ];

  return (
    <div
      className={cn(
        "rounded-lg overflow-hidden border border-border",
        className,
      )}
    >
      <MapContainer
        center={mapCenter}
        zoom={zoom}
        style={{ height, width: "100%" }}
        zoomControl={true}
      >
        <TileLayer
          attribution={MAP_CONFIG.TILE_LAYER_ATTRIBUTION}
          url={MAP_CONFIG.TILE_LAYER_URL}
        />
        {locations.map((location) => (
          <Marker
            key={location.index}
            position={[location.latitude, location.longitude]}
          >
            <Popup>
              {location.title}
              {location.popupContent && (
                <>
                  <br />
                  {location.popupContent}
                </>
              )}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}

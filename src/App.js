import React, { Component } from "react";
import { render } from "react-dom";
import {
  Map,
  TileLayer,
  Marker,
  Popup,
  LayersControl,
  FeatureGroup,
  GeoJSON
} from "react-leaflet";
import HeatmapLayer from "react-leaflet-heatmap-layer";
import boundary_json from "./data/ACT-Division-Boundaries.json";
import { summary } from "./data/expanded_summary.js";

class MyHeatMap extends Component {
  constructor() {
    super();

    this.position = [-35.325, 149.09];
    this.sliderValue = 5;

    this.getFeatureColor = this.getFeatureColor.bind(this);
    this.style = this.style.bind(this);
  }

  getFeatureColor = (feature) => {
    console.log(feature.properties.division_name)
    if (feature.properties.division_name == "PHILLIP") {
      return "green";
    } else {
      return "red";
    }
  }

  style(feature) {
    // console.log(feature.properties.division_name)
    return {
      fillColor: this.getFeatureColor(feature)
    };
  }

  onEachFeature(feature, layer) {
    
  }

  render() {
    return (
      <div id="map">
        <Map center={this.position} zoom={11.2}>
          <LayersControl>
            <LayersControl.BaseLayer name="Base" checked>
              <TileLayer
                url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                attribution="&copy; <a href=http://osm.org/copyright>OpenStreetMap</a> contributors"
              />
            </LayersControl.BaseLayer>

            <LayersControl.Overlay
              name="Boundaries"
              fitBoundsOnLoad
              fitBoundsOnUpdate
              checked
            >
              <GeoJSON
                data={boundary_json}
                onEachFeature={this.onEachFeature}
                style={this.style}
              />
            </LayersControl.Overlay>
          </LayersControl>
        </Map>
      </div>
    );
  }
}

export default MyHeatMap;

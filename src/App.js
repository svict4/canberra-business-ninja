import React, { Component } from "react";
import { render } from "react-dom";
import {
  Map,
  TileLayer,
  LayersControl,
  GeoJSON
} from "react-leaflet";
import boundary_json from "./data/ACT-Division-Boundaries.json";
import census_json from "./data/census.json";

class MyHeatMap extends Component {
  constructor() {
    super();

    this.position = [-35.325, 149.09];
    this.sliderValue = 5;

    this.colorFunction = this.colorFunction.bind(this);
    this.style = this.style.bind(this);
    this.getGradient = this.getGradient.bind(this);
  }

  // gradient color between green and red, accepts a float between 0 and 1
  getGradient(value){
    var hue=((1-value)*120).toString(10);
    return ["hsl(",hue,",100%,50%)"].join("");
  }

  colorFunction = (feature) => {
    //console.log(feature.properties.division_name)
    //this.props.age_intensity/100
    //this.props.income_intensity/100


    // if (feature.properties.division_name == "PHILLIP") {
    //   return "green";
    // } else {
    //   return "red";
    // }
  }

  style(feature) {
    // console.log(feature.properties.division_name)
    return {
      fillColor: this.colorFunction(feature)
    };
  }

  onEachFeature(feature, layer) {
    
  }

  componentWillUpdate() {
    //console.log(this.props.age_intensity/10);
    let ageArray = census_json.age[this.props.age_intensity/10];
    ageArrayMin = Math.min(...ageArray);
    ageArrayMax = Math.max(...ageArray);
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

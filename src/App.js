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
import summary_json from "./data/summary.json";

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
    var hue=(value*120).toString(10);
    return ["hsl(",hue,",100%,50%)"].join("");
  }

  colorFunction = (feature) => {    
    //this.props.age_intensity/100
    //this.props.income_intensity/100

    //console.log(feature.properties.division_name, summary_json[feature.properties.division_name].age[this.props.age_intensity/10]);
    let ageError = (summary_json[feature.properties.division_name].age[(this.props.age_intensity)/10+1] - this.props.age_intensity/100);
    let incomeError = summary_json[feature.properties.division_name].income[this.props.income_intensity/10+1] - [this.props.income_intensity/100]; 
    let quirkyError = summary_json[feature.properties.division_name].art.count - [this.props.quirky_intensity/100 + 50];


    // if (summary_json[feature.properties.division_name].art.count != undefined) {
    //   quirkyError = summary_json[feature.properties.division_name].art.count - [this.props.quirky_intensity/100]
    // }
    
    //console.log(this.props.quirky_intensity, summary_json[feature.properties.division_name].art[this.props.quirky_intensity/10+1])
    return this.getGradient((ageError + incomeError / 2) + quirkyError);
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
    // let ageArray = census_json.age[this.props.age_intensity/10];
    // let ageArrayMin = Math.min(...ageArray);
    // let ageArrayMax = Math.max(...ageArray);
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

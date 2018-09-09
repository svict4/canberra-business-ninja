import React, { Component }  from 'react'
import { render } from 'react-dom'
import MyHeatMap from './App'

import 'rc-slider/assets/index.css';
import 'rc-tooltip/assets/bootstrap.css';

import Tooltip from 'rc-tooltip';
import Slider from 'rc-slider';

import TextField from '@material-ui/core/TextField';
import DataConnector from './App';

const createSliderWithTooltip = Slider.createSliderWithTooltip;
const Range = createSliderWithTooltip(Slider.Range);

const Handle = Slider.Handle;

const marksAge = {
  0: "0-4",
  10: "5-14",
  20: "15-24",
  30: "25-34",
  40: "35-44",
  50: "45-54",
  60: "55-64",
  70: "65-74",
  80: "75-84",
  90: "85+"
};

class Controls extends Component {

  constructor()
  {
    super();
    this.state = {
      age_intensity: 50,
      income_intensity: 80
    };
  }

  handleChangeAge = (value) => {
    this.setState({
      age_intensity: value
    });
  }
  handleChangeIncome = (value) => {
    this.setState({
      income_intensity: value
    });
  }

  render() {
    return (
      <section className="banner fullscreen style1 orient-right content-align-left image-position-center onscroll-image-fade-in" id="first">

        <div className="content">
          <p>Every business is different and knowing your audience is important. Not all toldlers are looking to buy a SUV, not all centenarian are looking to buy schoolies nightclub tickets. Or are they?</p>

          <p>
          You know your business best. Our tool helps you find the next best place to help your business grow.
          </p>

          <h2>Who is your target market?</h2>

          <ul className="actions vertical">
            <li>
              Age
              <Slider step={10} max={90} dots range marks={marksAge} value={this.state.age_intensity} onChange={this.handleChangeAge} />
              {/* Weighting
              <TextField
                id="number"
                label="Number"
                value={this.state.age}
                onChange={this.handleChangeAge}
                type="number"
                InputLabelProps={{
                  shrink: true,
                }}
                margin="normal"
              /> */}
            </li>
            <li>
              Income
              <Slider step={10} dots value={this.state.income_intensity} onChange={this.handleChangeIncome} />
            </li>
          </ul>

          <p>Click on a subrub to get a closer look</p>

          <ul className="actions vertical">
            <li><a href="#third" className="button smooth-scroll-middle"> What's this voodoo magic? </a></li>
          </ul>
        </div>

        

        <div className="image" alt="">
            <MyHeatMap
            // age_intensity={this.state.age_intensity}
            // income_intensity={this.state.income_intensity}
           />
        </div>
        </section>
    );
  }

}

export default Controls;

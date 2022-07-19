import React, { Component } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import About from "../pages/About";




class Counter extends Component {
    styles = {
        fontSize: 40,
        fontWeight: "bold"
    };

    render() {
        return <React.Fragment>

            <h1 style={this.styles}>STONKTREK</h1>
            <button className="btn btn-secondary btn-sm">List of Trending Tickers</button>
        </React.Fragment>;
    }
}

export default Counter;
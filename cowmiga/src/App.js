import './App.css';
import React, { Component } from 'react';
import Gauge from './components/Gauge';
import Counter from './components/counter';
import Create from './components/Create';
import Stock from './components/Stock';
import List from './components/List'
import AddList from './components/AddList'
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import About from "./pages/About";
import Home from './pages/Home';
import Search from './pages/Search'



function App() {

  return (
    <div className="app">
      <Router>
        <nav>
          <Link to="/">Home</Link>
          <div></div>
          <Link to="/search">Search</Link>
          <div></div>
          <Link to="/about">About</Link>
        </nav>



        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Router>

      {/* <Stock /> */}

      {/* <Counter /> */}
      {/* <Create /> */}

      {/* <List /> */}
      {/* <AddList /> */}


      {/* <Gauge /> */}
    </div >
  );
}


export default App;
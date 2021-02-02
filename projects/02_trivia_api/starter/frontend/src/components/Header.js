import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className="app-header">
        <div className="app-logo" onClick={() => {this.navTo('')}}>Udacitrivia</div>
        <div
          className="header-link"
          onClick={() => {this.navTo('/add')}}
        >
          Add
        </div>
        <div
          className="header-link"
          onClick={() => {this.navTo('/play')}}
        >
          Play
        </div>
      </div>
    );
  }
}

export default Header;

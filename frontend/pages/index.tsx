import React, { Component } from "react";
import Header from './components/header.tsx'

type HomeState = {
  page: string,
}

class Home extends Component<{}, HomeState> {
  constructor(props) {
    super(props);
    this.state = {
        page: "home"
    };
  }

  handleClick (arg:string) {
    this.setState({page:arg})
  }
  render() {
    return (
      <div className="">
        <Header handleClick={this.handleClick}/>
      </div>
    )
  }
}

export default Home;
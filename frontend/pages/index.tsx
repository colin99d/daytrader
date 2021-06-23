import React, { Component } from "react";
import Header from './components/header.tsx'
import Table from './components/table.tsx'
import Home from './components/home.tsx'

type page = "home" | "table"
type stock = {id: number, ticker: string};
type algorithms = {id: number, name: string};
type decision = {
  id: number, 
  stock: stock, 
  algorithm:algorithms,
  openPrice: number,
  closingPrice: number,
  confidence: number,
  tradeDate: Date,
  created_at: Date
}

type HomeState = {
  page: page,
  stocks: stock[],
  decisions: decision[],
  error: string,
  baseUrl: string
}

class App extends Component<{}, HomeState> {
  constructor(props: any) {
    super(props);
    this.state = {
        page: "home",
        stocks: null,
        decisions: null,
        error: "",
        baseUrl: "http://http://192.168.1.72",
    };
    this.handleClick = this.handleClick.bind(this);
    this.getFetch = this.getFetch.bind(this);
  }

  getFetch(endpoint:string, state: "stocks" | "decisions") {
    fetch(this.state.baseUrl + endpoint)
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { error: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then((data: stock | decision) => this.setState({...this.state, [state]: data})
      );
  }

  handleClick (arg:page) {this.setState({page:arg})}

  componentDidMount() {
    this.getFetch("/api/stocks/", "stocks");
    this.getFetch("/api/decisions/", "decisions")
  }
  render() {
    let page;
    if (this.state.page =="home") {
      page = <Home stocks={this.state.stocks} baseUrl={this.state.baseUrl} getFetch={this.getFetch}/>;
    } else if (this.state.page == "table") {
      page = <Table decisions={this.state.decisions}/>;
    }
    return (
      <div className="h-screen">
        <Header handleClick={this.handleClick} page={this.state.page} />
        <div className="bg-gray-200 h-full">
          {page}
        </div>
      </div>
    )
  }
}

export default App;
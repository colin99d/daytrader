import React, { Component } from "react";
import Header from './components/header.tsx'
import Home from './components/home.tsx'

type stocks = {id: number, ticker: string}[];
type algorithms = {id: number, name: string}[];
type decisions = {
  id: number, 
  stock: number, 
  algorithm:number,
  openPrice: number,
  closingPrice: number,
  confidence: number,
  tradeDate: Date,
  created_at: Date
}[]

type HomeState = {
  page: string,
  stocks: stocks,
  decisions: decisions,
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
        baseUrl: "http://localhost:8000",
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
      .then((data: stocks | decisions) => this.setState({...this.state, [state]: data})
      );
  }

  handleClick (arg:string) {
    this.setState({page:arg})
  }

  componentDidMount() {
    this.getFetch("/api/stocks/", "stocks");
    this.getFetch("/api/decisions/", "decisions")
  }
  render() {
    return (
      <div className="h-screen">
        <Header handleClick={this.handleClick} page={this.state.page} />
        <div className="bg-gray-200 h-full">
          <Home stocks={this.state.stocks} baseUrl={this.state.baseUrl} getFetch={this.getFetch}/>
        </div>
      </div>
    )
  }
}

export default App;
import React, { Component } from "react";

import CashFlowGraph from './cashflowGraph';
import HedgingGraph from './hedgingGraph';
import Menu from './menu';

type portItem = {
    id: number,
    type: "stock" | "call" | "put",
    sign: -1 | 0 | 1,
    strike: number,
    cost: number
}

type option = {
    contractSymbol: string,
    strike: number,
    currency: string,
    lastPrice: number,
    change: number,
    percentChange: number,
    volume: number,
    openInterest: number,
    bid: number,
    ask: number,
    contractSize: string,
    expiration: number,
    lastTradeDate: number,
    impliedVolatility: number,
    inTheMoney: boolean,
}

type data = {
    cashflows: {id: string, data:{x:string,y:number}[]}[]
    info: {
        time: Date,
        price: number,
        volume: number
    }
    options: {
        expirations: number[],
        expiration: number,
        calls: option[],
        puts: option[]
    }
}

type HomeProps = {
    stocks: {id: number, ticker: string}[],
    baseUrl: string,
    getFetch: (endpoint:string, state: "stocks" | "decisions") => void
  }

type HomeState = {
    ticker: string,
    error: string,
    data: data,
    tickerDisplay: string,
    view: "hedging" | "cashflow",
    portfolio: portItem[],
}

class Home extends Component<HomeProps, HomeState> {
    constructor(props: any) {
        super(props);
        this.state = {
            ticker: "",
            error: "",
            data: null,
            tickerDisplay: "",
            view: "hedging",
            portfolio: [{id: 1, type: "stock", sign: 1, strike: null, cost: 0}],
        };
        this.handleAdd = this.handleAdd.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleErrors = this.handleErrors.bind(this);
        this.handleOptions = this.handleOptions.bind(this);
        this.handleRemove = this.handleRemove.bind(this);
        this.handlePortfolio = this.handlePortfolio.bind(this);
        this.changeView = this.changeView.bind(this);
      }
    handleChange(e: any, formKey:"ticker") {this.setState({...this.state, [formKey]: e.target.value})}

    handlePortfolio(id: number, key: "sign" | "type" | "strike", value: any,) {
        var oldItem: portItem = this.state.portfolio.find(item => item.id == id);
        //Refactor below
        if (key=="sign"){oldItem["sign"]=value.value}
        else if (key=="type"){oldItem["type"]=value.value}
        else if (key=="strike"){oldItem["strike"]=value.value}
        //Refactor above
        if (id > 1 && oldItem.sign != 0 ) {
            var newCost: number = this.state.data.options[oldItem.type + "s"].find(item => item.strike == oldItem.strike).lastPrice
            newCost *= oldItem.sign
            oldItem.cost = newCost;
        }
        var newPort = this.state.portfolio.filter(item => item.id != id);
        newPort.push(oldItem);
        this.setState({portfolio: newPort});
    }

    handleOptions(e: any) {
        var expDate: number = e.value;
        let url = this.props.baseUrl + "/cashflows/";
        let data  = new FormData();
        data.append('ticker', this.state.tickerDisplay);
        data.append('expiration', expDate.toString());
        fetch(url, {method: 'post',body: data,})
        .then(response => response.json())
        .then(data => {
            var oldData = this.state.data;
            oldData.options = data.options;
            this.setState({data: oldData})
        })
    }

    changeView(view: "hedging" | "cashflow") {this.setState({view: view})}

    handleErrors(response: any): any {
        if (!response.ok) {
            this.setState({error:response.statusText});
        }
        return response;
    }

    handleAdd() {
        if (this.state.data) {
            var ids: number[] = this.state.portfolio.map(item => item.id);
            var newId: number = Math.max(...ids) + 1;
            var portfolios = this.state.portfolio
            portfolios.push({id: newId, type:"call", sign: 1, strike: this.state.data.options.calls[0].strike, 
                cost: this.state.data.options.calls[0].lastPrice})
            this.setState({portfolio: portfolios})
        } 
    }

    handleRemove(id: number) {
        var newPort: portItem[] = this.state.portfolio.filter(item => item.id != id);
        this.setState({portfolio: newPort});
    }

    unixToDate(unix: number | "") {
        if (unix == null || unix == "") {
            return null
        }
        var dateObject = new Date (unix*1000);
        return dateObject.toLocaleDateString();
    }

    postGeneric(endpoint:string, data: { [name: string]: string } | FormData): Promise<any>  {
        return fetch(this.props.baseUrl + endpoint, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
          .then(this.handleErrors)
          .then(response => response.json())
    }

    handleClick(): void {
        let url = this.props.baseUrl + "/cashflows/";
        let data  = new FormData();
        data.append('ticker', this.state.ticker)
        fetch(url, {method: 'post',body: data,})
        .then(response => response.json())
        .then(data => {this.setState({data: data, tickerDisplay: this.state.ticker, ticker:""})})
    }

    render() {
        let expValue: number | "" = this.state.data ? this.state.data.options ? this.state.data.options.expiration : "" : ""
        let graph = this.state.view == "hedging"  ? <HedgingGraph data={this.state.data ? this.state.data.info : null} portfolio={this.state.portfolio}/> : 
            <CashFlowGraph data={this.state.data ? this.state.data.cashflows : null} />
      return (
        <div className="w-screen flex h-full">

            <Menu changeView={this.changeView} view={this.state.view} data={this.state.data} handleOptions={this.handleOptions} unixToDate={this.unixToDate}
                portfolio={this.state.portfolio} handlePortfolio={this.handlePortfolio} handleAdd={this.handleAdd} handleRemove={this.handleRemove} 
                error={this.state.error} ticker={this.state.ticker} handleClick={this.handleClick} handleChange={this.handleChange}/>
            <div className="ml-5 w-full h-5/6">
            {this.state.tickerDisplay ?  <h1 className="text-2xl font-bold leading-7 text-gray-900 text-center">{this.state.tickerDisplay.toUpperCase() + " - " + this.unixToDate(expValue)}</h1> : null}
           
            {graph}
    </div>
        </div>
  )
}
}

export default Home;

//
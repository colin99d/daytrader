import React, { Component } from "react";

type HomeProps = {
    stocks: {id: number, ticker: string}[],
    baseUrl: string,
    getFetch: (endpoint:string, state: "stocks" | "decisions") => void
  }

type HomeState = {
    ticker: string,
    error: string
}

class Home extends Component<HomeProps, HomeState> {
    constructor(props: any) {
        super(props);
        this.state = {
            ticker: "",
            error: "",
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
      }
      handleChange(e:any, formKey:"ticker") {this.setState({[formKey]: e.target.value})}

      handleErrors(response: any) {
        if (!response.ok) {
            throw Error(response.statusText);
        }
        return response;
    }

      handleClick(e:any) {
        if (this.state.ticker.length > 0) {
        fetch(this.props.baseUrl + "/api/stocks/", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ticker: this.state.ticker}),
          })
          .then(this.handleErrors)
          .then(response => response.json())
          .then(data => {
            console.log(data.status)
            console.log('Success:', data);
            this.props.getFetch("/api/stocks/", "stocks");
          })
          .catch((error) => {
            console.error('Error:', error);
          });
        } else {
            this.setState({error: "Cannot use a blank ticker."})
        }
        }

    render() {
      return (
        <div className="ml-3">
        <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">Asset Manager</h1>
        <form method="post" className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 lg:w-1/4 md:w-1/2">
            <p className="text-red-500">{this.state.error}</p>
            <label className="block text-gray-700 text-sm font-bold mb-2"></label>
            <input onChange={(e) => {this.handleChange(e, 'ticker')}} value={this.state.ticker} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" name="ticker" maxLength={5} />
            <button onClick={(e) => {this.handleClick(e)}} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4" type='button'>Submit</button>
        </form>

        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">Managed Assets</h2>

            <div className="bg-white shadow-xl rounded-lg lg:w-1/4 md:w-1/2">
                <ul className="divide-y divide-gray-300">
                    {this.props.stocks ? this.props.stocks.map( item => 
                    <li className="p-4 hover:bg-gray-50 cursor-pointer" key={item.id}>{item.ticker}</li>
                    ) : null}
                </ul>
            </div>
        </div>
  )
}
}

export default Home;
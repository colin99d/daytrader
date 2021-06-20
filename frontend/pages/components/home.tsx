import React, { Component } from "react";
import { ResponsiveLine } from '@nivo/line';

type HomeProps = {
    stocks: {id: number, ticker: string}[],
    baseUrl: string,
    getFetch: (endpoint:string, state: "stocks" | "decisions") => void
  }

type HomeState = {
    ticker: string,
    error: string,
    data: any  //update
}

class Home extends Component<HomeProps, HomeState> {
    constructor(props: any) {
        super(props);
        this.state = {
            ticker: "",
            error: "",
            data: "",
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleActivate = this.handleActivate.bind(this);
        this.handleClick = this.handleClick.bind(this);
      }
      handleChange(e:any, formKey:"ticker") {this.setState({[formKey]: e.target.value})}

    handleErrors(response: any) {
        if (!response.ok) {
            throw Error(response.statusText);
        }
        return response;
    }

    postGeneric(endpoint:string, data: { [name: string]: string }): Promise<any>  {
        return fetch(this.props.baseUrl + endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
          .then(this.handleErrors)
          .then(response => response.json())
    }

    handleClick() {
        if (this.state.ticker.length > 0) {
            this.postGeneric("/api/stocks/",{ticker: this.state.ticker})
            .then(() => this.props.getFetch("/api/stocks/", "stocks"))
        } else {
            this.setState({error: "Cannot use a blank ticker."})
        }
    }

    handleActivate(ticker: string) {
        this.postGeneric("/cashflows/",{ticker: ticker})
        .then(data => {this.setState({data: data})})
    }

    render() {
      return (
        <div className="ml-3 w-screen flex h-full">
            <div>
            <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">Asset Manager</h1>
            <form method="post" className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <p className="text-red-500">{this.state.error}</p>
                <label className="block text-gray-700 text-sm font-bold mb-2"></label>
                <input onChange={(e) => {this.handleChange(e, 'ticker')}} value={this.state.ticker} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" name="ticker" maxLength={5} />
                <button onClick={() => {this.handleClick()}} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4" type='button'>Submit</button>
            </form>

            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">Managed Assets</h2>

                <div className="bg-white shadow-xl rounded-lg">
                    <ul className="divide-y divide-gray-300">
                        {this.props.stocks ? this.props.stocks.map( item => 
                        <li onClick={() => {this.handleActivate(item.ticker)}} className="p-4 hover:bg-gray-50 cursor-pointer" key={item.id}>{item.ticker}</li>
                        ) : null}
                    </ul>
                </div>
                </div>
            <div className="ml-5 h-3/4 w-full">
            <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">Chart</h1>
            {this.state.data ?<ResponsiveLine
            data={this.state.data}
        margin={{ top: 50, right: 160, bottom: 50, left: 60 }}
        xScale={{
            type: 'time',
            format: '%m-%d-%Y',
            precision: 'year',
            }}
        yScale={{ type: 'linear', stacked: true }}
        yFormat=" >-.2f"
        curve="monotoneX"
        axisTop={null}
        axisBottom={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            format: '.2f',
            legend: 'Date',
            legendOffset: 36,
            legendPosition: 'middle'
        }}
        axisLeft={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            format: '.2s',
            legend: 'Cash Flows',
            legendOffset: -40,
            legendPosition: 'middle'
        }}
        enableGridX={false}
        colors={{ scheme: 'spectral' }}
        lineWidth={1}
        pointSize={4}
        pointColor={{ theme: 'background' }}
        pointBorderWidth={1}
        pointBorderColor={{ from: 'serieColor' }}
        pointLabelYOffset={-12}
        useMesh={true}
        gridXValues={[ 0, 20, 40, 60, 80, 100, 120 ]}
        gridYValues={[ 0, 500, 1000, 1500, 2000, 2500 ]}
        legends={[
            {
                anchor: 'bottom-right',
                direction: 'column',
                justify: false,
                translateX: 140,
                translateY: 0,
                itemsSpacing: 2,
                itemDirection: 'left-to-right',
                itemWidth: 80,
                itemHeight: 12,
                itemOpacity: 0.75,
                symbolSize: 12,
                symbolShape: 'circle',
                symbolBorderColor: 'rgba(0, 0, 0, .5)',
                effects: [
                    {
                        on: 'hover',
                        style: {
                            itemBackground: 'rgba(0, 0, 0, .03)',
                            itemOpacity: 1
                        }
                    }
                ]
            }
        ]}
    /> : null}
    </div>
        </div>
  )
}
}

export default Home;
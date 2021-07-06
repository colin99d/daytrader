import React, { Component } from "react";
import { ResponsiveLine } from '@nivo/line';

const theme={
    axis: {
      ticks: {
        text: {
          fontSize: 16,
        }
      }
    }
  }

type data = {id: string, data:{x:string,y:number}[]}

type HomeProps = {
    stocks: {id: number, ticker: string}[],
    baseUrl: string,
    getFetch: (endpoint:string, state: "stocks" | "decisions") => void
  }

type HomeState = {
    ticker: string,
    error: string,
    data: data[],
    tickerDisplay: string
}

class Home extends Component<HomeProps, HomeState> {
    constructor(props: any) {
        super(props);
        this.state = {
            ticker: "",
            error: "",
            data: null,
            tickerDisplay: "",
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleErrors = this.handleErrors.bind(this);
      }
      handleChange(e:any, formKey:"ticker") {this.setState({[formKey]: e.target.value})}

    handleErrors(response: any): any {
        if (!response.ok) {
            this.setState({error:response.statusText});
        }
        return response;
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

    formatNumber(value: number): string {
        if (value == 0) {
            return "$" + value.toString();
        } else if ((Math.abs(value) / 1000000000000) > 1) {
            return "$" + (value / 1000000000000).toString() + "T"
        } else if ((Math.abs(value) / 1000000000) > 1) {
            return "$" + (value / 1000000000).toString() + "B"
        } else if ((Math.abs(value) / 1000000) > 1) {
            return "$" + (value / 1000000).toString() + "M"
        } else if ((Math.abs(value) / 1000) > 1) {
            return "$" + (value / 1000).toString() + "K"
        }
    }

    getTickerDates(): Date[] {
        var dates: Date[] = [];
        this.state.data.forEach(item => {
            item["data"].forEach(subItem => {
                dates.push(new Date(subItem["x"]));
            })
        })
        return Array.from(new Set(dates));
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
                </div>
            <div className="ml-5 h-3/4 w-full">
            <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate text-center">{this.state.tickerDisplay.toUpperCase()}</h1>
            {this.state.data ?<div className="w-full h-full bg-white">
            <ResponsiveLine 
                theme={theme}
                data={this.state.data}
                margin={{ top: 50, right: 50, bottom: 100, left: 65 }}
                xScale={{ format: "%m-%d-%Y", type: "time" }}
                yScale={{ type: 'linear', stacked: false, min:"auto", max:"auto"}}
                xFormat="time:%m-%d-%Y"
                yFormat=">-$,.2f"
                curve="monotoneX"
                axisTop={null}
                axisBottom={{
                    tickValues: this.getTickerDates(),
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    format: "%m-%d-%Y",
                    legendOffset: 36,
                    legendPosition: "middle"
                }}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    format: d => this.formatNumber(d),
                    legendOffset: -45,
                    legendPosition: 'middle'
                }}
                enableGridX={false}
                colors={{ scheme: 'spectral' }}
                lineWidth={3}
                pointSize={6}
                pointColor={{ theme: 'background' }}
                pointBorderWidth={1}
                pointBorderColor={{ from: 'serieColor' }}
                pointLabelYOffset={-12}
                useMesh={true}
                legends={[
                    {
                        anchor: 'bottom-left',
                        direction: 'column',
                        justify: false,
                        translateX: 0,
                        translateY: 90,
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
            /></div> : null}
    </div>
        </div>
  )
}
}

export default Home;
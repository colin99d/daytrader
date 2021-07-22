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

type data =  {
    id: string, 
    data:{x:string,y:number}[]
}

type HomeProps = {
    data: data[]
  }

class CashFlowGraph extends Component<HomeProps, {} >{
    constructor(props: any) {
        super(props);
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
        this.props.data.forEach(item => {
            item["data"].forEach(subItem => {
                dates.push(new Date(subItem["x"]));
            })
        })
        return Array.from(new Set(dates));
    }

    render() {
      return (
        <div className= "w-full h-full">
            {this.props.data ?<div className="w-full h-full bg-white">
            <ResponsiveLine 
                theme={theme}
                data={this.props.data}
                margin={{ top: 50, right: 50, bottom: 100, left: 65 }}
                xScale={{ format: "%m-%d-%Y", type: "time" }}
                yScale={{ type: 'linear', stacked: false, min:"auto", max:"auto"}}
                xFormat="time:%m-%d-%Y"
                yFormat=">-$,.2f"
                curve="monotoneX"
                axisTop={null}
                axisBottom={{
                    tickValues: this.getTickerDates(), //custom formula
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
                    format: d => this.formatNumber(d),  //custom formula
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
  )
}
}

export default CashFlowGraph;
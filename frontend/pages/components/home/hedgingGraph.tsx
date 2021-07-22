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

type HomeProps = {
    data: {
        time: Date,
        price: number,
        volume: number
    }
    portfolio: {id: number, type: string, sign: number,}[]
  }

class HedgingGraph extends Component<HomeProps, {} >{
    constructor(props: any) {
        super(props);
      }

    dataFunction(step: number) {
      var main = this.props.portfolio.find(item => item.id == 1);
      console.log(main.sign);
      return step * main.sign;
    }

    generateData() {
        var base: number = this.props.data.price;
        var looper = Array.from(Array(25).keys())
        var beforeFees = [];
        var breakEven = [];
        looper.forEach((item, idx) => {
          var step: number = 0.02;
          var nextX: number = base * idx * step
          var change: number = base * idx * this.dataFunction(step);
          beforeFees.push({"x" : base + nextX, "y": base + change});
          beforeFees.push({"x" : base - nextX, "y": base - change});
          breakEven.push({"x" : base + nextX, "y": base});
          breakEven.push({"x" : base - nextX, "y": base});
        })
        return [{id: "Before Fees", data: beforeFees},{id: "Break Even", color: "hsl(27, 0%, 85%)", data: breakEven}]
    }

    render() {
        let values = this.props.data ? this.generateData() : null
      return (
        <div className= "w-full h-full">
            {this.props.data ?<div className="w-full h-full bg-white">
            <ResponsiveLine 
                theme={theme}
                data={values}
                margin={{ top: 50, right: 50, bottom: 100, left: 65 }}
                xScale={{ type: 'linear', stacked: false, min:"auto", max:"auto"}}
                yScale={{ type: 'linear', stacked: false, min:"auto", max:"auto"}}
                xFormat=">-$r"
                yFormat=">-$r"
                curve="linear"
                axisTop={null}
                axisBottom={{
                    //tickValues: this.getTickerDates()
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    //format: "%m-%d-%Y",
                    legendOffset: 36,
                    legendPosition: "middle"
                }}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    //format: d => this.formatNumber(d),  //custom formula
                    legendOffset: -45,
                    legendPosition: 'middle'
                }}
                enableGridX={false}
                //colors={{ scheme: 'spectral' }}
                lineWidth={3}
                enablePoints={false}
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

export default HedgingGraph;
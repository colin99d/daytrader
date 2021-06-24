import React, { Component } from "react";

type ForumProps = {
    message: string,
  }

class Forum extends Component<ForumProps, {}> {

    render() {
      return (
        <div className="flex flex-row py-4 px-2 items-center border-b-2">
        <div className="w-1/4">
            <img src="https://source.unsplash.com/otT2199XwI8/600x600" className="object-cover h-12 w-12 rounded-full" alt=""/>
        </div>
        <div className="w-full">
            <div className="text-lg font-semibold">Everest Trip 2021</div>
            <span className="text-gray-500">Hi Sam, Welcome</span>
        </div>
        
        </div>
  )
}
}


class Chat extends Component<{}, {}> {
    constructor(props: any) {
        super(props);
        this.state = {
        };
      }

    render() {
      return (
        <div className="mx-auto shadow-lg rounded-lg mt-1 h-full">
            <div className="flex flex-row justify-between bg-white h-full">
            <div className="flex flex-col w-2/5 border-r-2 overflow-y-auto">
                <div className="border-b-2 py-4 px-2">
                <input type="text" placeholder="search chatting" className="py-2 px-2 border-2 border-gray-200 rounded-2xl w-full"/>
                </div>

                <Forum message={'ur mom'}/>


            </div>
            <div className="w-full px-5 flex flex-col justify-between">
                <div className="flex flex-col mt-5">
                <div className="flex justify-end mb-4">
                    <div
                    className="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
                    >
                    Welcome to group everyone !
                    </div>
                    <img
                    src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                    className="object-cover h-8 w-8 rounded-full"
                    alt=""
                    />
                </div>
                <div className="flex justify-start mb-4">
                    <img
                    src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                    className="object-cover h-8 w-8 rounded-full"
                    alt=""
                    />
                    <div
                    className="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-white"
                    >
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat
                    at praesentium, aut ullam delectus odio error sit rem. Architecto
                    nulla doloribus laborum illo rem enim dolor odio saepe,
                    consequatur quas?
                    </div>
                </div>
                <div className="flex justify-end mb-4">
                    <div>
                    <div
                        className="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
                    >
                        Lorem ipsum dolor, sit amet consectetur adipisicing elit.
                        Magnam, repudiandae.
                    </div>

                    <div
                        className="mt-4 mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
                    >
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Debitis, reiciendis!
                    </div>
                    </div>
                    <img
                    src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                    className="object-cover h-8 w-8 rounded-full"
                    alt=""
                    />
                </div>
                <div className="flex justify-start mb-4">
                    <img
                    src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
                    className="object-cover h-8 w-8 rounded-full"
                    alt=""
                    />
                    <div
                    className="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-white"
                    >
                    happy holiday guys!
                    </div>
                </div>
                </div>
                <div className="py-5">
                <input
                    className="w-full bg-gray-300 py-5 px-3 rounded-xl"
                    type="text"
                    placeholder="type your message here..."
                />
                </div>
            </div>
            </div>
            </div>
       
  )
}
}

export default Chat;
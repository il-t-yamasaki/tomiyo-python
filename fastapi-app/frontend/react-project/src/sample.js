import React from "react";
import axios from "axios";

class Sample extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        message1 : ''
        };
    }

    handleClick = () => {
        const url = "http://localhost:80/";
        axios.request({
            method: 'post',
            url,
            data: {
                    "ID": "005",
                    "Name": "hoge",
                    "Class": "x"
                }
            })
            .then(res => {
                this.setState();
            })
            .catch(err =>{
                console.log(err);
            });
    };

    render() {
        return (
        <dev>
            <button onClick={this.handleClick}>POST</button>
            <p>メッセージ</p>
        </dev>
        );
    }
}

export default Sample;
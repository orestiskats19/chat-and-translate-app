import React, {useState, useEffect} from 'react';
import './Bubble.css';

function Bubble(message) {

    useEffect(() => {

    }, []);


    return <>
        {/*<div className={"container1"}>*/}
        {message.props.direction === "right" ?
            <li className="me">
                <div className={"test"}>
                    <div className={"line"}>{message.props.text}</div>
                    <div>{message.props.translation}</div>
                </div>
            </li> :
            <li className="him">
                <div>
                <div className={"line"}>{message.props.text}</div>
                <div>{message.props.translation}</div>
            </div>
            </li>}

        {/*</div>*/}
    </>
}

export default Bubble;

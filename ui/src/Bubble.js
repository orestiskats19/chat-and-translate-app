import React, {useState, useEffect} from 'react';
import './Bubble.css';

function Bubble(message) {

    return <>
            <li className={message.props.direction === "3" ? "me":"him"}>
                <div className={"test"}>
                    <div className={"line"}>{message.props.text}</div>
                    <div>{message.props.translation}</div>
                </div>
            </li>
    </>
}

export default Bubble;

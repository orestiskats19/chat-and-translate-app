import React, {useState, useEffect} from 'react';
import './Bubble.css';

function Bubble(message) {

    return <>
        <div className={"http://localhost:3000/"}>
            <li className={message.props.direction === "3" ? "me":"him"}>
                <div className={"test"}>
                    <div className={"line"}>{message.props.text}</div>
                    <div>{message.props.translation}</div>
                </div>
            </li>
    </div>
        </>
}

export default Bubble;

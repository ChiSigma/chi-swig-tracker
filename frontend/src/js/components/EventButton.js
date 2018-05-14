/**
 * Created by alexmelagrano on 5/14/18.
 */
import React from 'react';

export default class EventButton extends React.Component {

    handleClick(e) {
        console.log('handling click to add a new event of type: ' + this.props.eventType);
        this.props.newDrinkEvent(this.props.eventType);
    }

    render() {
        return (
            <button className="btn btn-success p-1" onClick={ this.handleClick.bind(this) } >
                +
            </button>
        )
    }
}

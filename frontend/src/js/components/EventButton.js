/**
 * Created by alexmelagrano on 5/14/18.
 */
import React from 'react';
import FontAwesome from 'react-fontawesome';

export default class EventButton extends React.Component {

    handleClick(e) {
        e.stopPropagation();
        this.props.newDrinkEvent(this.props.eventType['id']);
    }

    render() {
        return (
            <FontAwesome 
                name={ this.props.eventType['icon'] }
                onClick={ this.handleClick.bind(this) } 
                className={ "event-button " + this.props.color }
            />
        );
    }
}

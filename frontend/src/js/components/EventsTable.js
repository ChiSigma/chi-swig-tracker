import React from 'react';

import EventButton from './EventButton';

export default class EventsTable extends React.Component {
    countsForEventType(eventType) {
        return this.props.eventTimes.map((time) =>
            <td>
                {this.props.events[eventType][time]}
            </td>
        )
    }

    render() {
        const tableHeaders = () => {
            let tableData = '<thead><tr>'; 
            for (var eventTime in this.props.eventTime) {
                tableData += '<th>' + eventTime + '</th>'
            }
            return tableData + '</tr></thead>'
        }

        const eventTimes = this.props.eventTimes.map((time) =>
            <th>{time}</th>
        );

        const showEventButtons = function(component) {
            if (!this.props.isEditable()) return;

            return component;
        }.bind(this);

        const buttonColor = this.props.isUpvoteMode() ? "font-green" : "font-red";
        const addOrDelete = this.props.isUpvoteMode() ? "+1" : "-1";

        const eventRows = Object.keys(this.props.events).map((eventType) =>
            <tr>
                { showEventButtons((<td>
                             <EventButton color={ buttonColor } newDrinkEvent={ this.props.newDrinkEvent.bind(this) } eventType={ this.props.eventTypes[eventType] } />
                            </td>)) }
                <th>
                    {eventType}
                </th>
                { this.countsForEventType(eventType) }
            </tr>
        );

        return (
            <table className={ this.props.classes }>
                <thead>
                    <tr>
                        { showEventButtons((<th>{ addOrDelete }</th>)) }
                        <th>Event Type</th>
                        { eventTimes }
                    </tr>
                    { eventRows }
                </thead>
            </table>
        )
    }
}
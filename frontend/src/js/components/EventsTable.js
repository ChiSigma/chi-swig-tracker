import React from 'react';

import EventButton from './EventButton';

export default class EventsTable extends React.Component {
    constructor(props) {
        super(props);
    }

    countsForEventType(eventType) {
        return this.props.eventTimes.map((time) =>
            <td>
                {this.props.events[eventType][time]}
            </td>
        )
    }

    render() {
        // TODO :: use this.props.eventTypes to build the action icons
        const tableHeaders = () => {
            let tableData = '<thead><tr>'; 
            for (var eventTime in this.props.eventTime) {
                tableData += '<th>' + eventTime + '</th>'
            }
            return tableData + '</tr></thead>'
        }
        

        // for (var eventType in this.state.eventData) {
        //     if (!this.state.eventData.hasOwnProperty(eventType)) {
        //         continue;
        //     }

        //     let button = '<td>' + <EventButton newDrinkEvent={ this.newDrinkEvent.bind(this) } eventType={ this.props.eventTypes[eventType] } /> + '</td>';
        //     let rowTitle = '<th>' + eventType + '</th>';
        //     let rowAllTime = '<td>' + this.state.eventData[eventType]["All Time"] + '</td>';
        //     let rowPastDay = '<td>' + this.state.eventData[eventType]["Past Day"] + '</td>';
        //     let rowPastWeek = '<td>' + this.state.eventData[eventType]["Past Week"] + '</td>';
        //     tableData += '<tr>' + button + rowTitle + rowAllTime + rowPastDay + rowPastWeek + '</tr>';
        // }

        const eventTimes = this.props.eventTimes.map((time) =>
            <th>{time}</th>
        );

        const buttonColor = this.props.isUpvoteMode() ? "font-green" : "font-red";

        const eventRows = Object.keys(this.props.events).map((eventType) =>
            <tr>
                <td>
                    <EventButton color={ buttonColor } newDrinkEvent={ this.props.newDrinkEvent.bind(this) } eventType={ this.props.eventTypes[eventType] } />
                </td>
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
                        <th>+1</th>
                        <th>Event Type</th>
                        { eventTimes }
                    </tr>
                    { eventRows }
                </thead>
            </table>
        )
    }
}
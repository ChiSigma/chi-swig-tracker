/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class SortWidget extends React.Component {
    constructor() {
        super();
        this.sortOrder = 'time';
    }

    changeSort(e) {
        this.sortOrder = e.target.value;
        console.log('changing sort order to ' + e.target.value);
        // TODO :: make request to sort endpoint
    }

    render() {
        return (
            <div className="d-flex align-items-center">
                <p className="mr-2 mb-0">Sort By:</p>
                <select onChange={this.changeSort.bind(this)} >
                    <option>Event Type</option>
                    <option>Time</option>
                    <option>Order</option>
                </select>
            </div>
        )
    }
}

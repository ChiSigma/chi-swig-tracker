/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class SortWidget extends React.Component {
    constructor() {
        super();
        const startDate = new Date("2018-05-24T22:58:05.939Z");
        const now = new Date();
        const secondsSince = Math.abs(now - startDate) / 1000;
        const daysSince = Math.floor(secondsSince / 86400);
        this.state = {
            timeLive: daysSince
        }
    }

    render() {
        return (
            <div>
                <p className="mr-2 mb-0">Total Days: {this.state.timeLive} days</p>
            </div>
        )
    }
}

/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class SortWidget extends React.Component {
    constructor() {
        super();

        // TODO :: make this an endpoint? or do clientside?
        this.state = {timeLive: '0'};
    }

    render() {
        return (
            <div>
                <p className="mr-2 mb-0">Total Days: {this.state.timeLive} days</p>
            </div>
        )
    }
}

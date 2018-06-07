/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class SortWidget extends React.Component {
    changeSort(e) {
        const targetValue = e.target.value.split(',');
        const sortEventType = targetValue[0];
        const sortTime = targetValue[1];

        this.props.context.state.updateSort(sortEventType, sortTime);
    }

    render() {
        return (
            <div className="d-flex align-items-center">
                <select onChange={this.changeSort.bind(this)} >
                    <option value={ [1, '*'] }>Sort By: Total Drinks All Time</option>
                    <option value={ [1, '7d'] }>Sort By: Total Drinks This Week</option>
                    <option value={ [1, '24h'] }>Sort By: Total Drinks Today</option>
                </select>
            </div>
        )
    }
}

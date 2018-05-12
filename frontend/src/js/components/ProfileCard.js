/**
 * Created by alexmelagrano on 5/11/18.
 */
import React from 'react';

import crestIcon from '../../assets/crestIcon.png';

export default class ProfileCard extends React.Component {
    constructor(props) {
        super(props);

        // TODO :: given [this.props.activeProfile], get drinker events data
        // using dummy data for now
        this.profileInfo = {
            "Blacked Out": {
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            },
            "Cleaned": {
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            },
            "Cooked": {
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            },
            "Drank": {
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            },
            "Puked": {
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            }
        };

        // TODO :: given [this.props.activeProfile], get drinker profile photo url
        this.profilePhoto = 'https://media.licdn.com/dms/image/C4E03AQHzXHptRd-cHg/profile-displayphoto-shrink_200_200/0?e=1531353600&v=beta&t=A5jkjzccz4PBvdNXggFFPwavsEorI6rXot2eRLn-iaY';
    }

    render() {
        let tableData = '<thead><tr><th>Event Type</th><th>All Time</th><th>Past Day</th><th>Past Week</th></tr></thead>';
        for (var eventType in this.profileInfo) {
            if (!this.profileInfo.hasOwnProperty(eventType)) {
                continue;
            }
            let rowTitle = '<th>' + eventType + '</th>';
            let rowAllTime = '<td>' + this.profileInfo[eventType]["All Time"] + '</td>';
            let rowPastDay = '<td>' + this.profileInfo[eventType]["Past Day"] + '</td>';
            let rowPastWeek = '<td>' + this.profileInfo[eventType]["Past Week"] + '</td>';
            tableData += '<tr>' + rowTitle + rowAllTime + rowPastDay + rowPastWeek + '</tr>';
        }

        return (
            <div className="profile-card flipper">
                <div className="card-front shadow-lg bg-plus p-3">
                    <div className="bg-red rounded-corners p-1">
                        <img src={ this.profilePhoto } alt="profile_photo_active"
                             className="border-med border-dark rounded-corners w-100"/>
                    </div>
                    <div className="bg-white border-med border-dark rounded-circle position-absolute card-icon">
                        <img src={ crestIcon } width="50px" alt="Chi_Sigma_Crest_Icon"/>
                    </div>
                    <div className="text-uppercase mt-4">
                        <h4 className="text-black-50 mb-1">First Name</h4>
                        <h2 className="text-red mb-0">Last Name</h2>
                    </div>
                </div>
                <div className="card-back shadow-lg bg-plus p-3">
                    <div className="bg-red rounded-circle position-absolute card-icon p-1">
                        <img src={ this.profilePhoto } width="50px" alt="profile_photo_active"
                             className="border-med border-dark rounded-circle "/>
                    </div>
                    <div className="text-uppercase ml-1 mt-3">
                        <h4 className="text-black-50 mb-1">First Name</h4>
                        <h2 className="text-red mb-0">Last Name</h2>
                    </div>
                    <div className="bg-white border border-dark rounded m-1 p-2">
                        <table className="table mb-0" dangerouslySetInnerHTML={{ __html: tableData }} />
                    </div>
                    <div className="p-2">
                        <span className="font-weight-bold">Highlight Reel</span>
                        <i className="text-black-50 small d-block">"I smell like lemonssss."</i>
                    </div>
                </div>
            </div>
        )
    }
}

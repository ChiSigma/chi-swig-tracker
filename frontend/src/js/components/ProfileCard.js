/**
 * Created by alexmelagrano on 5/11/18.
 */
import React from 'react';

import crestIcon from '../../assets/crestIcon.png';
import EventButton from './EventButton';

export default class ProfileCard extends React.Component {
    constructor(props) {
        super(props);

        // this.response = // TODO :: make request to /api/drinkers/[this.props.profile["id"]]/events/
        // using dummy data for now
        this.eventData = {
            "Blacked Out": {
                "id": 3,
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            },
            "Cleaned": {
                "id": 4,
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            },
            "Cooked": {
                "id": 5,
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            },
            "Drank": {
                "id": 1,
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            },
            "Puked": {
                "id": 2,
                "All Time": 3,
                "Past Day": 0,
                "Past Week": 0
            }
        };
    }
    
    newDrinkEvent(eventTypeID) {
        console.log('new drink event of type: ' + eventTypeID);
        // TODO :: make request to /api/drinkers/[this.props.profile["id"]]/[eventTypeID]/
    }

    render() {
        // Definitely a better, more React-ish way to do this but it works for now
        // TODO :: use this.props.eventTypes to build the action icons
        let tableData = '<thead><tr><th>Event Type</th><th>All Time</th><th>Past Day</th><th>Past Week</th></tr></thead>';
        for (var eventType in this.eventData) {
            if (!this.eventData.hasOwnProperty(eventType)) {
                continue;
            }

            let button = '<td>' + <EventButton newDrinkEvent={ this.newDrinkEvent.bind(this) } eventType={ this.eventData[eventType]["id"] } /> + '</td>';
            let rowTitle = '<th>' + eventType + '</th>';
            let rowAllTime = '<td>' + this.eventData[eventType]["All Time"] + '</td>';
            let rowPastDay = '<td>' + this.eventData[eventType]["Past Day"] + '</td>';
            let rowPastWeek = '<td>' + this.eventData[eventType]["Past Week"] + '</td>';
            tableData += '<tr>' + button + rowTitle + rowAllTime + rowPastDay + rowPastWeek + '</tr>';
        }

        // TODO :: uncomment the following block to enable privacy settings
         let tableClasses = "table mb-0";
        // if (!this.props.profile["is_public"]) {
        //    tableClasses += 'mask-values';
        // }

        // TODO :: const profilePhoto = this.props.profile["profile_photo"];
        const profilePhoto = 'https://media.licdn.com/dms/image/C4E03AQHzXHptRd-cHg/profile-displayphoto-shrink_200_200/0?e=1531353600&v=beta&t=A5jkjzccz4PBvdNXggFFPwavsEorI6rXot2eRLn-iaY';
        // TODO :: const bio = this.props.profile["bio_line"];
        const bio = 'I smell like lemonssss.';
        // TODO :: const name = this.props.profile["name"];
        const name = 'Melons';

        return (
            <div className="profile-card flipper">
                <div className="card-front shadow-lg bg-plus p-3">
                    <div className="bg-red rounded-corners p-1">
                        <img src={ profilePhoto } alt="profile_photo_active"
                             className="border-med border-dark rounded-corners w-100"/>
                    </div>
                    <div className="bg-white border-med border-dark rounded-circle position-absolute card-icon">
                        <img src={ crestIcon } width="50px" alt="Chi_Sigma_Crest_Icon"/>
                    </div>
                    <div className="text-uppercase mt-4">
                        <h4 className="text-black-50 mb-1">First Name</h4>
                        <h2 className="text-red mb-0">{ name }</h2>
                    </div>
                </div>
                <div className="card-back shadow-lg bg-plus p-3">
                    <div className="bg-red rounded-circle position-absolute card-icon p-1">
                        <img src={ profilePhoto } width="50px" alt="profile_photo_active"
                             className="border-med border-dark rounded-circle "/>
                    </div>
                    <div className="text-uppercase ml-1 mt-3">
                        <h4 className="text-black-50 mb-1">First Name</h4>
                        <h2 className="text-red mb-0">{ name }</h2>
                    </div>
                    <div className="bg-white border border-dark rounded m-1 p-2">
                        <table className={ tableClasses } dangerouslySetInnerHTML={{ __html: tableData }} />
                    </div>
                    <div className="p-2">
                        <span className="font-weight-bold">Highlight Reel</span>
                        <i className="text-black-50 small d-block">{ bio }</i>
                    </div>
                </div>
            </div>
        )
    }
}
